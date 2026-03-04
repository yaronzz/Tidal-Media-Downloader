"""TIDAL API helpers — media instantiation, name builders, pagination."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING

from tidalapi import Album, Mix, Playlist, Session, Track, UserPlaylist, Video
from tidalapi.artist import Artist, Role
from tidalapi.media import MediaMetadataTags, Quality
from tidalapi.user import LoggedInUser

from tidal_dl.constants import FAVORITES, MediaType
from tidal_dl.helper.exceptions import MediaUnknown

if TYPE_CHECKING:
    from tidal_dl.helper.cache import TTLCache


def name_builder_artist(media: Track | Video | Album, delimiter: str = ", ") -> str:
    """Return a delimited string of artist names for the given media.

    Args:
        media (Track | Video | Album): Media object.
        delimiter (str): Delimiter between names. Defaults to ", ".

    Returns:
        str: Delimited artist names.
    """
    return delimiter.join(artist.name for artist in media.artists)


def name_builder_album_artist(
    media: Track | Album,
    first_only: bool = False,
    delimiter: str = ", ",
) -> str:
    """Return a delimited string of main album artist names.

    Args:
        media (Track | Album): Media object.
        first_only (bool): Only include the first main artist. Defaults to False.
        delimiter (str): Delimiter between names. Defaults to ", ".

    Returns:
        str: Delimited album artist names.
    """
    artists_tmp: list[str] = []
    artists: list[Artist] = media.album.artists if isinstance(media, Track) else media.artists

    for artist in artists:
        if Role.main in artist.roles:
            artists_tmp.append(artist.name)

            if first_only:
                break

    return delimiter.join(artists_tmp)


def name_builder_title(media: Track | Video | Mix | Playlist | Album) -> str:
    """Return the display title for a media object.

    Args:
        media: Any TIDAL media object.

    Returns:
        str: Display title.
    """
    return media.title if isinstance(media, Mix) else media.full_name if hasattr(media, "full_name") else media.name


def name_builder_item(media: Track | Video) -> str:
    """Return 'Artist(s) - Title' string for a track or video.

    Args:
        media (Track | Video): Media object.

    Returns:
        str: Formatted name string.
    """
    return f"{name_builder_artist(media)} - {name_builder_title(media)}"


def get_tidal_media_id(url_or_id_media: str) -> str:
    """Extract the media ID from a TIDAL URL or return the value as-is.

    Args:
        url_or_id_media (str): Full TIDAL URL or bare ID.

    Returns:
        str: Media ID.
    """
    id_dirty = url_or_id_media.rsplit("/", 1)[-1]
    return id_dirty.rsplit("?", 1)[0]


def get_tidal_media_type(url_media: str) -> MediaType | bool:
    """Determine the MediaType from a TIDAL URL.

    Args:
        url_media (str): Full TIDAL URL.

    Returns:
        MediaType | bool: Detected media type or False if unrecognised.
    """
    result: MediaType | bool = False
    url_split = url_media.split("/")[-2]

    if len(url_split) > 1:
        media_name = url_media.split("/")[-2]

        _map = {
            "track": MediaType.TRACK,
            "video": MediaType.VIDEO,
            "album": MediaType.ALBUM,
            "playlist": MediaType.PLAYLIST,
            "mix": MediaType.MIX,
            "artist": MediaType.ARTIST,
        }
        result = _map.get(media_name, False)

    return result


def url_ending_clean(url: str) -> str:
    """Strip trailing '/u' or '?u' from a TIDAL URL.

    Args:
        url (str): URL to clean.

    Returns:
        str: Cleaned URL.
    """
    return url[:-2] if url.endswith("/u") or url.endswith("?u") else url


def instantiate_media(
    session: Session,
    media_type: MediaType,
    id_media: str,
    cache: TTLCache | None = None,
) -> Track | Video | Album | Playlist | Mix | Artist:
    """Create a TIDAL media object for the given type and ID.

    When *cache* is provided the result is looked up in the cache first.  On a
    cache miss the object is fetched from the TIDAL API and stored for reuse
    within the current session (avoids redundant HTTP calls when the same
    media ID is requested multiple times, e.g. all tracks of an album).

    Args:
        session (Session): Active TIDAL session.
        media_type (MediaType): Type of the media.
        id_media (str): Media ID.
        cache (TTLCache | None): Optional response cache. Defaults to None.

    Returns:
        A TIDAL media object.

    Raises:
        MediaUnknown: If the media type is not recognised.
    """
    cache_key = f"{media_type}:{id_media}"

    if cache is not None:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    if media_type == MediaType.TRACK:
        result = session.track(id_media, with_album=True)
    elif media_type == MediaType.VIDEO:
        result = session.video(id_media)
    elif media_type == MediaType.ALBUM:
        result = session.album(id_media)
    elif media_type == MediaType.PLAYLIST:
        result = session.playlist(id_media)
    elif media_type == MediaType.MIX:
        result = session.mix(id_media)
    elif media_type == MediaType.ARTIST:
        result = session.artist(id_media)
    else:
        raise MediaUnknown

    if cache is not None:
        cache.set(cache_key, result)

    return result


def items_results_all(
    media_list: Mix | Playlist | Album | Artist,
    videos_include: bool = True,
) -> list[Track | Video | Album]:
    """Fetch all items in a collection, handling pagination.

    Args:
        media_list: A TIDAL collection object.
        videos_include (bool): Include videos when fetching playlists/albums.

    Returns:
        list: All media items.
    """
    result: list[Track | Video | Album] = []

    if isinstance(media_list, Mix):
        result = media_list.items()
    else:
        func_get_items_media: list[Callable] = []

        if isinstance(media_list, Playlist | Album):
            func_get_items_media.append(media_list.items if videos_include else media_list.tracks)
        else:
            func_get_items_media.append(media_list.get_albums)
            func_get_items_media.append(media_list.get_ep_singles)

        result = paginate_results(func_get_items_media)

    return result


def paginate_results(
    func_get_items_media: list[Callable],
) -> list[Track | Video | Album | Playlist | UserPlaylist]:
    """Paginate through all results from one or more list-fetching callables.

    Args:
        func_get_items_media (list[Callable]): Callables that accept limit/offset kwargs.

    Returns:
        list: All collected items.
    """
    result: list = []

    for func_media in func_get_items_media:
        limit = 50 if func_media.__func__ == LoggedInUser.playlist_and_favorite_playlists else 100
        offset = 0
        done = False

        while not done:
            tmp_result = func_media(limit=limit, offset=offset)

            if tmp_result:
                result += tmp_result
                offset += limit
                # Small delay between pagination pages to avoid rapid-fire API calls.
                time.sleep(0.5)
            else:
                done = True

    return result


def all_artist_album_ids(media_artist: Artist) -> list[int | None]:
    """Return all album IDs for an artist (albums + EPs/singles).

    Args:
        media_artist (Artist): TIDAL Artist object.

    Returns:
        list[int | None]: List of album IDs.
    """
    albums: list[Album] = paginate_results([media_artist.get_albums, media_artist.get_ep_singles])
    return [album.id for album in albums]


def quality_audio_highest(media: Track | Album) -> Quality:
    """Return the highest available audio quality for a track or album.

    Args:
        media (Track | Album): TIDAL media object.

    Returns:
        Quality: Highest available quality enum value.
    """
    if MediaMetadataTags.hi_res_lossless in media.media_metadata_tags:
        return Quality.hi_res_lossless
    elif MediaMetadataTags.lossless in media.media_metadata_tags:
        return Quality.high_lossless
    else:
        return media.audio_quality


def favorite_function_factory(tidal: object, favorite_item: str) -> Callable:
    """Return the tidalapi callable for fetching a favorites collection.

    Args:
        tidal: Tidal config object with a .session attribute.
        favorite_item (str): Key from FAVORITES constant dict.

    Returns:
        Callable: The function to call to fetch the favorites list.
    """
    function_name: str = FAVORITES[favorite_item]["function_name"]
    return getattr(tidal.session.user.favorites, function_name)
