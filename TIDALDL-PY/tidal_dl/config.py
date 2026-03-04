"""Configuration management for tidal-dl.

Provides:
  - Settings: User preferences singleton backed by settings.json.
  - Tidal: TIDAL session singleton with OAuth login and Dolby Atmos credential switching.
  - HandlingApp: Application-lifecycle events (abort / run).
"""

import contextlib
import json
import os
import shutil
from collections.abc import Callable
from json import JSONDecodeError
from pathlib import Path
from threading import Event, Lock
from typing import Any

import tidalapi
import typer
from rich.console import Console as RichConsole

_console = RichConsole()

from tidal_dl import api as _api
from tidal_dl.constants import (
    ATMOS_CLIENT_ID,
    ATMOS_CLIENT_SECRET,
    ATMOS_REQUEST_QUALITY,
)
from tidal_dl.helper.cache import TTLCache
from tidal_dl.helper.decorator import SingletonMeta
from tidal_dl.helper.path import path_config_base, path_file_settings, path_file_token
from tidal_dl.model.cfg import Settings as ModelSettings
from tidal_dl.model.cfg import Token as ModelToken


class BaseConfig:
    """Base class for JSON-backed configuration objects."""

    data: ModelSettings | ModelToken
    file_path: str
    cls_model: type
    path_base: str = path_config_base()

    def save(self, config_to_compare: str | None = None) -> None:
        """Persist current config to disk.

        Args:
            config_to_compare (str | None): If provided, skip write when unchanged.
        """
        data_json = self.data.to_json()

        if config_to_compare == data_json:
            return

        os.makedirs(self.path_base, exist_ok=True)

        with open(self.file_path, encoding="utf-8", mode="w") as f:
            json.dump(json.loads(data_json), f, indent=4)

    def set_option(self, key: str, value: Any) -> None:
        """Set a configuration option, coercing type as needed.

        Args:
            key (str): Attribute name on the data model.
            value: New value (will be coerced to match the existing type).
        """
        value_old: Any = getattr(self.data, key)

        if type(value_old) is bool:
            value = value.lower() in ("true", "1", "yes", "y") if isinstance(value, str) else bool(value)
        elif type(value_old) is int and not isinstance(value, int):
            value = int(value)

        setattr(self.data, key, value)

    def read(self, path: str) -> bool:
        """Load configuration from a JSON file.

        Args:
            path (str): Path to the JSON config file.

        Returns:
            bool: True if the file was loaded successfully.
        """
        result: bool = False
        settings_json: str = ""

        try:
            with open(path, encoding="utf-8") as f:
                settings_json = f.read()

            self.data = self.cls_model.from_json(settings_json)
            result = True
        except (JSONDecodeError, TypeError, FileNotFoundError, ValueError) as e:
            if isinstance(e, ValueError):
                path_bak = path + ".bak"

                if os.path.exists(path_bak):
                    os.remove(path_bak)

                shutil.move(path, path_bak)
                print(
                    "Something is wrong with your config. It may be incompatible with this version. "
                    f"A backup was saved to '{path_bak}' and a new default config was created."
                )

            self.data = self.cls_model()

        self.save(settings_json)

        return result


class Settings(BaseConfig, metaclass=SingletonMeta):
    """Singleton holding user preferences loaded from settings.json."""

    def __init__(self) -> None:
        self.cls_model = ModelSettings
        self.file_path = path_file_settings()
        self.read(self.file_path)


class Tidal(BaseConfig, metaclass=SingletonMeta):
    """Singleton wrapping a tidalapi Session with OAuth and Dolby Atmos support."""

    session: tidalapi.Session
    token_from_storage: bool = False
    settings: Settings
    is_pkce: bool
    api_cache: TTLCache
    _active_key_index: int

    def __init__(self, settings: Settings | None = None) -> None:
        self.cls_model = ModelToken
        tidal_config = tidalapi.Config(item_limit=10000)
        self.session = tidalapi.Session(tidal_config)
        self.original_client_id = self.session.config.client_id
        self.original_client_secret = self.session.config.client_secret
        # Serialize all stream-fetch operations to prevent race conditions
        # when switching between Atmos and normal session credentials.
        self.stream_lock = Lock()
        self.is_pkce = False
        self.is_atmos_session = False
        self._active_key_index = 0
        self.file_path = path_file_token()
        self.token_from_storage = self.read(self.file_path)

        # Apply the first valid API key from the managed key list.
        self._apply_api_key(0)

        # Initialise the response cache (TTL applied after settings load).
        ttl = settings.data.api_cache_ttl_sec if settings else 300
        self.api_cache = TTLCache(ttl_sec=ttl)

        if settings:
            self.settings = settings
            self.settings_apply()

    def settings_apply(self, settings: Settings | None = None) -> bool:
        """Apply quality settings from the Settings singleton to the session.

        Args:
            settings (Settings | None): If provided, replace stored settings.

        Returns:
            bool: Always True.
        """
        if settings:
            self.settings = settings

        if not self.is_atmos_session:
            self.session.audio_quality = tidalapi.Quality(self.settings.data.quality_audio)

        self.session.video_quality = tidalapi.VideoQuality.high

        return True

    # ------------------------------------------------------------------
    # API key management
    # ------------------------------------------------------------------

    def _apply_api_key(self, index: int) -> bool:
        """Apply the API key at *index* from the managed key list to the session config.

        Args:
            index (int): Zero-based index into the key list returned by :mod:`tidal_dl.api`.

        Returns:
            bool: True if a valid key was applied, False if index is out of range or invalid.
        """
        key = _api.getItem(index)
        if key.get("valid") != "True" or not key.get("clientId"):
            return False

        self.session.config.client_id = key["clientId"]
        self.session.config.client_secret = key["clientSecret"]
        self._active_key_index = index
        return True

    def _try_login_with_key_rotation(self) -> bool:
        """Attempt token login, rotating through all available API keys on failure.

        Iterates :func:`tidal_dl.api.getItems` in order.  The first key that
        allows a successful ``login_token()`` call wins and is recorded as the
        active key.  Falls back to the original ``tidalapi`` credentials if
        the managed list is exhausted.

        Returns:
            bool: True if login succeeded with any key.
        """
        keys = _api.getItems()

        for index, key in enumerate(keys):
            if key.get("valid") != "True" or not key.get("clientId"):
                continue

            self._apply_api_key(index)

            if self.login_token(do_pkce=self.is_pkce):
                _console.print(
                    f"[dim]API key [{index}] ({key.get('platform', 'unknown')}) accepted.[/dim]"
                )
                return True

            _console.print(
                f"[yellow]API key [{index}] ({key.get('platform', 'unknown')}) failed, trying next...[/yellow]"
            )

        # All managed keys exhausted — restore original tidalapi credentials
        # and attempt one final login with them.
        self.session.config.client_id = self.original_client_id
        self.session.config.client_secret = self.original_client_secret
        return self.login_token(do_pkce=self.is_pkce)

    def login_token(self, do_pkce: bool = False) -> bool:
        """Attempt to restore a session from a stored token.

        Args:
            do_pkce (bool): Use PKCE flow. Defaults to False.

        Returns:
            bool: True if the session was restored.
        """
        self.is_pkce = do_pkce
        result = False

        if self.token_from_storage:
            try:
                result = self.session.load_oauth_session(
                    self.data.token_type,
                    self.data.access_token,
                    self.data.refresh_token,
                    self.data.expiry_time,
                    is_pkce=do_pkce,
                )
            except Exception:
                result = False

                if os.path.exists(self.file_path):
                    os.remove(self.file_path)

                print(
                    "Either there is something wrong with your credentials / account or some server problems on TIDAL's "
                    "side. Try logging in again by re-running this app."
                )

        return result

    def login_finalize(self) -> bool:
        """Check and persist a newly-established login session.

        Returns:
            bool: True if login was successful.
        """
        result = self.session.check_login()

        if result:
            self.token_persist()

        return result

    def token_persist(self) -> None:
        """Save the current session token to disk."""
        self.set_option("token_type", self.session.token_type)
        self.set_option("access_token", self.session.access_token)
        self.set_option("refresh_token", self.session.refresh_token)
        self.set_option("expiry_time", self.session.expiry_time)
        self.save()

        with contextlib.suppress(OSError, NotImplementedError):
            os.chmod(self.file_path, 0o600)

    def switch_to_atmos_session(self) -> bool:
        """Re-authenticate the session with Dolby Atmos credentials.

        Returns:
            bool: True if successful or already in Atmos mode.
        """
        if self.is_atmos_session:
            return True

        _console.print("[cyan]Switching session context to Dolby Atmos...[/cyan]")
        self.session.config.client_id = ATMOS_CLIENT_ID
        self.session.config.client_secret = ATMOS_CLIENT_SECRET
        self.session.audio_quality = ATMOS_REQUEST_QUALITY

        if not self.login_token(do_pkce=self.is_pkce):
            _console.print("[yellow]Warning:[/yellow] Atmos session authentication failed.")
            self.restore_normal_session(force=True)
            return False

        self.is_atmos_session = True
        _console.print("[cyan]Session is now in Atmos mode.[/cyan]")
        return True

    def restore_normal_session(self, force: bool = False) -> bool:
        """Restore the session to original user credentials.

        Args:
            force (bool): Force restoration even if already in normal mode.

        Returns:
            bool: True if successful or already in normal mode.
        """
        if not self.is_atmos_session and not force:
            return True

        _console.print("[cyan]Restoring session context to Normal...[/cyan]")
        # Restore the active managed key (not the raw tidalapi default),
        # so the session stays consistent with the key that succeeded at login.
        if not self._apply_api_key(self._active_key_index):
            self.session.config.client_id = self.original_client_id
            self.session.config.client_secret = self.original_client_secret
        self.session.audio_quality = tidalapi.Quality(self.settings.data.quality_audio)

        if not self.login_token(do_pkce=self.is_pkce):
            _console.print("[yellow]Warning:[/yellow] Restoring original session failed. Please restart the application.")
            return False

        self.is_atmos_session = False
        _console.print("[cyan]Session is now in Normal mode.[/cyan]")
        return True

    def login(self, fn_print: Callable) -> bool:
        """Perform an interactive login.

        Tries the stored token first (rotating through managed API keys on
        failure); if all keys fail, launches a device-link OAuth flow.
        The browser is opened automatically; a clickable fallback link is also
        printed for headless / SSH environments.

        Args:
            fn_print (Callable): Output function for user messages.

        Returns:
            bool: True if logged in successfully.
        """
        is_token = self._try_login_with_key_rotation()

        if is_token:
            fn_print("Yep, looks good! You are logged in.")
            return True

        fn_print("You either do not have a token or your token is invalid.")
        fn_print("No worries, we will handle this...")

        # Use the lower-level login_oauth() so we can open the browser ourselves
        # before blocking on future.result().
        link_login, future = self.session.login_oauth()
        url: str = f"https://{link_login.verification_uri_complete}"

        # Try to auto-open the browser; fall back gracefully on headless systems.
        try:
            typer.launch(url)
            _console.print(f"[green]Browser opened.[/green] If it did not open, visit:")
        except Exception:
            _console.print("[yellow]Could not open browser automatically.[/yellow] Visit:")

        _console.print(
            f"  [link={url}][bold cyan]{url}[/bold cyan][/link]\n"
            f"  [dim]Link expires in {link_login.expires_in} seconds.[/dim]"
        )

        future.result()  # blocks until the user completes the browser login
        is_login = self.login_finalize()

        if is_login:
            fn_print("The login was successful. I have stored your credentials (token).")
            return True

        fn_print("Something went wrong. Did you complete the browser login? You may try again.")
        return False

    def logout(self) -> bool:
        """Remove the stored token and invalidate the current session.

        Returns:
            bool: Always True.
        """
        Path(self.file_path).unlink(missing_ok=True)
        self.token_from_storage = False
        del self.session
        return True


class HandlingApp(metaclass=SingletonMeta):
    """Singleton that owns the application abort / run events."""

    event_abort: Event = Event()
    event_run: Event = Event()

    def __init__(self) -> None:
        self.event_run.set()
