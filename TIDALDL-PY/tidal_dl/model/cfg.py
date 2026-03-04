from dataclasses import dataclass

from dataclasses_json import dataclass_json
from tidalapi import Quality

from tidal_dl.constants import CoverDimensions, InitialKey, MetadataTargetUPC, QualityVideo


@dataclass_json
@dataclass
class Settings:
    skip_existing: bool = True
    lyrics_embed: bool = False
    lyrics_file: bool = False
    use_primary_album_artist: bool = False
    video_download: bool = True
    download_delay: bool = True
    download_base_path: str = "~/download"
    quality_audio: Quality = Quality.low_320k
    quality_video: QualityVideo = QualityVideo.P480
    download_dolby_atmos: bool = False
    format_album: str = "Albums/{album_artist}/{album_title}/{track_volume_num_optional_CD}/{track_title}"
    format_playlist: str = "- Playlists/{playlist_name}/{list_pos}. {artist_name} - {track_title}"
    format_mix: str = "Mix/{mix_name}/{artist_name} - {track_title}"
    format_track: str = "Tracks/{album_artist}/{album_title}/{track_title}"
    format_video: str = "Videos/{artist_name}/{track_title}"
    video_convert_mp4: bool = True
    path_binary_ffmpeg: str = ""
    metadata_cover_dimension: CoverDimensions = CoverDimensions.Px320
    metadata_cover_embed: bool = True
    mark_explicit: bool = False
    cover_album_file: bool = True
    extract_flac: bool = True
    downloads_simultaneous_per_track_max: int = 20
    download_delay_sec_min: float = 3.0
    download_delay_sec_max: float = 5.0
    album_track_num_pad_min: int = 1
    downloads_concurrent_max: int = 3
    symlink_to_track: bool = False
    playlist_create: bool = False
    metadata_replay_gain: bool = False
    metadata_write_url: bool = True
    metadata_delimiter_artist: str = ", "
    metadata_delimiter_album_artist: str = ", "
    filename_delimiter_artist: str = ", "
    filename_delimiter_album_artist: str = ", "
    metadata_target_upc: MetadataTargetUPC = MetadataTargetUPC.UPC
    api_rate_limit_batch_size: int = 20
    api_rate_limit_delay_sec: float = 3.0
    initial_key_format: InitialKey = InitialKey.ALPHANUMERIC
    skip_duplicate_isrc: bool = True
    api_cache_enabled: bool = True
    api_cache_ttl_sec: int = 300


@dataclass_json
@dataclass
class HelpSettings:
    skip_existing: str = "Skip download if file already exists."
    lyrics_embed: str = "Embed lyrics in audio file, if lyrics are available."
    use_primary_album_artist: str = "Use only the primary album artist for folder paths instead of track artists."
    lyrics_file: str = "Save lyrics to separate *.lrc file, if lyrics are available."
    video_download: str = "Allow download of videos."
    download_delay: str = "Activate randomized download delay to mimic human behaviour."
    download_base_path: str = "Where to store the downloaded media."
    quality_audio: str = (
        'Desired audio download quality: "LOW" (96kbps), "HIGH" (320kbps), '
        '"LOSSLESS" (16 Bit, 44,1 kHz), "HI_RES_LOSSLESS" (up to 24 Bit, 192 kHz)'
    )
    quality_video: str = 'Desired video download quality: "360", "480", "720", "1080"'
    download_dolby_atmos: str = "Download Dolby Atmos audio streams if available."
    format_album: str = "Where to download albums and how to name the items."
    format_playlist: str = "Where to download playlists and how to name the items."
    format_mix: str = "Where to download mixes and how to name the items."
    format_track: str = "Where to download tracks and how to name the items."
    format_video: str = "Where to download videos and how to name the items."
    video_convert_mp4: str = (
        "Videos are downloaded as MPEG Transport Stream (TS) files. "
        "With this option each video will be converted to MP4. FFmpeg must be installed."
    )
    path_binary_ffmpeg: str = (
        "Path to FFmpeg binary file (executable). Only necessary if FFmpeg is not set in $PATH. "
        "Mandatory for Windows: The directory of ffmpeg.exe must be set in %PATH%."
    )
    metadata_cover_dimension: str = (
        "The square dimensions of the cover image embedded into the track. "
        "Possible values: 80, 160, 320, 640, 1280, origin."
    )
    metadata_cover_embed: str = "Embed album cover into file."
    mark_explicit: str = "Mark explicit tracks with '[E]' in track title (only applies to metadata)."
    cover_album_file: str = "Save cover to 'cover.jpg', if an album is downloaded."
    extract_flac: str = "Extract FLAC audio tracks from MP4 containers and save them as *.flac (uses FFmpeg)."
    downloads_simultaneous_per_track_max: str = "Maximum number of simultaneous chunk downloads per track."
    download_delay_sec_min: str = "Lower boundary for the calculation of the download delay in seconds."
    download_delay_sec_max: str = "Upper boundary for the calculation of the download delay in seconds."
    album_track_num_pad_min: str = (
        "Minimum length of the album track count, will be padded with zeroes (0). "
        "To disable padding set this to 1."
    )
    downloads_concurrent_max: str = "Maximum concurrent number of downloads (threads)."
    symlink_to_track: str = (
        "If enabled the tracks of albums, playlists and mixes will be downloaded to the track directory "
        "but symlinked accordingly."
    )
    playlist_create: str = "Creates a '_playlist.m3u' file for downloaded albums, playlists and mixes."
    metadata_replay_gain: str = "Replay gain information will be written to metadata."
    metadata_write_url: str = "URL of the media file will be written to metadata."
    metadata_delimiter_artist: str = "Metadata tag delimiter for multiple artists. Default: ', '"
    metadata_delimiter_album_artist: str = "Metadata tag delimiter for multiple album artists. Default: ', '"
    filename_delimiter_artist: str = "Filename delimiter for multiple artists. Default: ', '"
    filename_delimiter_album_artist: str = "Filename delimiter for multiple album artists. Default: ', '"
    metadata_target_upc: str = (
        "Select the target metadata tag ('UPC', 'BARCODE', 'EAN') where to write the UPC information to. "
        "Default: 'UPC'."
    )
    api_rate_limit_batch_size: str = "Number of albums to process before applying rate limit delay."
    api_rate_limit_delay_sec: str = "Delay in seconds between batches to avoid API rate limiting."
    initial_key_format: str = "Format for Initial Key metadata tag: 'alphanumeric' (default) or 'classic'."
    skip_duplicate_isrc: str = (
        "Skip download if a track with the same ISRC was already downloaded to any path. "
        "Uses a persistent index at ~/.config/tidal-dl/isrc_index.json."
    )
    api_cache_enabled: str = (
        "Cache TIDAL API responses in-memory during a session to reduce redundant HTTP calls. "
        "Especially effective when downloading albums (avoids re-fetching the same album object per track)."
    )
    api_cache_ttl_sec: str = (
        "Time-to-live in seconds for each cached API response. "
        "Entries older than this value are discarded and re-fetched. Default: 300 (5 minutes)."
    )


@dataclass_json
@dataclass
class Token:
    token_type: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expiry_time: float = 0.0
