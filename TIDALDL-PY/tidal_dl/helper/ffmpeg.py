"""FFmpeg detection and OS-aware installation helper."""

import platform
import shutil
import subprocess

from rich.console import Console

_console = Console()


def find_ffmpeg() -> str | None:
    """Locate the ffmpeg binary on the system PATH.

    Returns:
        str | None: Absolute path to ffmpeg, or None if not found.
    """
    return shutil.which("ffmpeg")


def _detect_linux_package_manager() -> tuple[str, list[str]] | None:
    """Detect the available Linux package manager and return its install command.

    Returns:
        tuple[str, list[str]] | None: (manager name, install command list) or None.
    """
    managers = [
        ("apt", ["sudo", "apt", "install", "-y", "ffmpeg"]),
        ("dnf", ["sudo", "dnf", "install", "-y", "ffmpeg"]),
        ("pacman", ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"]),
        ("zypper", ["sudo", "zypper", "install", "-y", "ffmpeg"]),
        ("apk", ["sudo", "apk", "add", "ffmpeg"]),
    ]

    for name, cmd in managers:
        if shutil.which(name):
            return name, cmd

    return None


def get_install_info() -> tuple[str, list[str]] | None:
    """Return the OS-appropriate package manager name and install command.

    Returns:
        tuple[str, list[str]] | None: (description, command list) or None if unsupported.
    """
    system = platform.system()

    if system == "Windows":
        if shutil.which("winget"):
            return "winget", ["winget", "install", "--id", "Gyan.FFmpeg", "-e", "--accept-source-agreements"]
        elif shutil.which("choco"):
            return "Chocolatey", ["choco", "install", "ffmpeg", "-y"]
        elif shutil.which("scoop"):
            return "Scoop", ["scoop", "install", "ffmpeg"]
        return None

    elif system == "Darwin":
        if shutil.which("brew"):
            return "Homebrew", ["brew", "install", "ffmpeg"]
        return None

    elif system == "Linux":
        return _detect_linux_package_manager()

    return None


def install_ffmpeg() -> str:
    """Install ffmpeg using the system package manager.

    This is mandatory — the application cannot function correctly without
    ffmpeg.  If automatic installation fails, the function raises
    ``SystemExit`` with instructions for manual installation.

    Returns:
        str: Absolute path to the ffmpeg binary.

    Raises:
        SystemExit: If ffmpeg could not be installed or found after install.
    """
    info = get_install_info()

    if info is None:
        _console.print(
            "[red bold]FFmpeg is required but could not be installed automatically.[/red bold]\n"
            "No supported package manager was detected.\n"
            "Please install FFmpeg manually: [link=https://ffmpeg.org/download.html]https://ffmpeg.org/download.html[/link]"
        )
        raise SystemExit(1)

    manager_name, install_cmd = info
    cmd_display = " ".join(install_cmd)

    _console.print(
        f"\n[cyan]FFmpeg is required but was not found — installing automatically.[/cyan]\n"
        f"Package manager: [bold]{manager_name}[/bold]\n"
        f"Running: [dim]{cmd_display}[/dim]"
    )

    try:
        subprocess.run(install_cmd, check=True)
    except FileNotFoundError:
        _console.print(
            f"[red bold]Package manager '{manager_name}' was not found.[/red bold]\n"
            "Please install FFmpeg manually: [link=https://ffmpeg.org/download.html]https://ffmpeg.org/download.html[/link]"
        )
        raise SystemExit(1)
    except subprocess.CalledProcessError as e:
        _console.print(
            f"[red bold]FFmpeg installation failed (exit code {e.returncode}).[/red bold]\n"
            "Please install FFmpeg manually: [link=https://ffmpeg.org/download.html]https://ffmpeg.org/download.html[/link]"
        )
        raise SystemExit(1)

    # Verify the binary is now available.
    path = find_ffmpeg()

    if path:
        _console.print(f"[green]FFmpeg installed successfully:[/green] {path}")
        return path

    _console.print(
        "[red bold]Installation command succeeded but ffmpeg was not found on PATH.[/red bold]\n"
        "You may need to restart your terminal and try again."
    )
    raise SystemExit(1)
