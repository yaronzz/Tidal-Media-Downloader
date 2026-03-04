import pathlib
from dataclasses import dataclass, field
from enum import StrEnum

from requests import HTTPError
from tidalapi.media import Stream, StreamManifest


class DownloadOutcome(StrEnum):
    """Result of a single item download."""

    DOWNLOADED = "downloaded"
    SKIPPED = "skipped"
    FAILED = "failed"
    UNAVAILABLE = "unavailable"


@dataclass
class DownloadSummary:
    """Aggregate outcome counters for a collection download."""

    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    unavailable: int = 0

    @property
    def total(self) -> int:
        return self.downloaded + self.skipped + self.failed + self.unavailable

    def record(self, outcome: DownloadOutcome) -> None:
        if outcome == DownloadOutcome.DOWNLOADED:
            self.downloaded += 1
        elif outcome == DownloadOutcome.SKIPPED:
            self.skipped += 1
        elif outcome == DownloadOutcome.UNAVAILABLE:
            self.unavailable += 1
        else:
            self.failed += 1


@dataclass
class DownloadSegmentResult:
    result: bool
    url: str
    path_segment: pathlib.Path
    id_segment: int
    error: HTTPError | None = None


@dataclass
class TrackStreamInfo:
    """Container for track stream information."""

    stream_manifest: StreamManifest | None
    file_extension: str
    requires_flac_extraction: bool
    media_stream: Stream | None
