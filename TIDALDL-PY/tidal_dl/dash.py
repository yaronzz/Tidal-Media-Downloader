"""Utilities for parsing TIDAL DASH manifests.

This module contains a light-weight set of data structures that mimic the
``dash+xml`` schema exposed by the upstream python-tidal project.  The classes
only implement the behaviour required by the downloader which focuses on
audio representations and the URLs required to fetch the segment media.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Union
from urllib.parse import urljoin
from xml.etree import ElementTree


@dataclass
class SegmentTimelineEntry:
    start_time: Optional[int]
    duration: int
    repeat: int = 0


@dataclass
class SegmentTemplate:
    media: Optional[str]
    initialization: Optional[str]
    start_number: int = 1
    timescale: int = 1
    presentation_time_offset: int = 0
    timeline: List[SegmentTimelineEntry] = field(default_factory=list)


@dataclass
class SegmentList:
    initialization: Optional[str]
    media_segments: List[str] = field(default_factory=list)


@dataclass
class Representation:
    id: Optional[str]
    bandwidth: Optional[str]
    codec: Optional[str]
    base_url: str
    segment_template: Optional[SegmentTemplate]
    segment_list: Optional[SegmentList]

    @property
    def segments(self) -> List[str]:
        if self.segment_list is not None:
            return _build_segment_list(self.segment_list, self.base_url)
        if self.segment_template is not None:
            return _build_segment_template(self.segment_template, self.base_url, self)
        return []


@dataclass
class AdaptationSet:
    content_type: Optional[str]
    base_url: str
    representations: List[Representation] = field(default_factory=list)


@dataclass
class Period:
    base_url: str
    adaptation_sets: List[AdaptationSet] = field(default_factory=list)


@dataclass
class Manifest:
    base_url: str
    periods: List[Period] = field(default_factory=list)


def parse_manifest(xml: Union[str, bytes]) -> Manifest:
    """Parse a DASH manifest into structured objects."""

    if isinstance(xml, bytes):
        xml_text = xml.decode("utf-8")
    else:
        xml_text = str(xml)

    xml_text = re.sub(r'xmlns="[^"]+"', '', xml_text, count=1)
    root = ElementTree.fromstring(xml_text)

    manifest_base = _get_base_url(root, '')
    manifest = Manifest(base_url=manifest_base)

    for period_el in root.findall('Period'):
        manifest.periods.append(_parse_period(period_el, manifest_base))
    return manifest


def _parse_period(element: ElementTree.Element, parent_base: str) -> Period:
    base_url = _get_base_url(element, parent_base)
    period = Period(base_url=base_url)

    for adaptation_el in element.findall('AdaptationSet'):
        period.adaptation_sets.append(_parse_adaptation(adaptation_el, base_url))
    return period


def _parse_adaptation(element: ElementTree.Element, parent_base: str) -> AdaptationSet:
    base_url = _get_base_url(element, parent_base)
    adaptation = AdaptationSet(content_type=element.get('contentType'), base_url=base_url)

    for rep_el in element.findall('Representation'):
        adaptation.representations.append(_parse_representation(rep_el, base_url))
    return adaptation


def _parse_representation(element: ElementTree.Element, parent_base: str) -> Representation:
    base_url = _get_base_url(element, parent_base)
    template = element.find('SegmentTemplate')
    seg_template = _parse_segment_template(template) if template is not None else None

    seg_list_el = element.find('SegmentList')
    seg_list = _parse_segment_list(seg_list_el) if seg_list_el is not None else None

    return Representation(
        id=element.get('id'),
        bandwidth=element.get('bandwidth'),
        codec=element.get('codecs'),
        base_url=base_url,
        segment_template=seg_template,
        segment_list=seg_list,
    )


def _parse_segment_template(element: ElementTree.Element) -> SegmentTemplate:
    template = SegmentTemplate(
        media=element.get('media'),
        initialization=element.get('initialization'),
        start_number=int(element.get('startNumber') or 1),
        timescale=int(element.get('timescale') or 1),
        presentation_time_offset=int(element.get('presentationTimeOffset') or 0),
    )

    timeline_el = element.find('SegmentTimeline')
    if timeline_el is not None:
        for s_el in timeline_el.findall('S'):
            duration = int(s_el.get('d'))
            repeat = int(s_el.get('r') or 0)
            start_time = int(s_el.get('t')) if s_el.get('t') else None
            template.timeline.append(SegmentTimelineEntry(start_time=start_time, duration=duration, repeat=repeat))
    return template


def _parse_segment_list(element: ElementTree.Element) -> SegmentList:
    init_el = element.find('Initialization')
    initialization = init_el.get('sourceURL') if init_el is not None else None

    media_segments = []
    for seg_el in element.findall('SegmentURL'):
        media = seg_el.get('media')
        if media:
            media_segments.append(media)

    return SegmentList(initialization=initialization, media_segments=media_segments)


def _build_segment_template(template: SegmentTemplate, base_url: str, representation: Representation) -> List[str]:
    segments: List[str] = []

    if template.initialization:
        segments.append(_complete_url(template.initialization, base_url, representation))

    number = template.start_number
    current_time: Optional[int] = None
    for entry in template.timeline:
        if entry.start_time is not None:
            current_time = entry.start_time
        elif current_time is None:
            current_time = template.presentation_time_offset

        for _ in range(entry.repeat + 1):
            media = template.media
            if media:
                segments.append(
                    _complete_url(media, base_url, representation, number=number, time=current_time)
                )
            number += 1
            if current_time is not None:
                current_time += entry.duration

    return segments


def _build_segment_list(segment_list: SegmentList, base_url: str) -> List[str]:
    segments: List[str] = []

    if segment_list.initialization:
        segments.append(urljoin(base_url, segment_list.initialization))

    for media in segment_list.media_segments:
        segments.append(urljoin(base_url, media))

    return segments


def _complete_url(
    template: str,
    base_url: str,
    representation: Representation,
    *,
    number: Optional[int] = None,
    time: Optional[int] = None,
) -> str:
    mapping = {
        '$RepresentationID$': representation.id,
        '$Bandwidth$': representation.bandwidth,
        '$Number$': None if number is None else str(number),
        '$Time$': None if time is None else str(time),
    }

    result = template
    for placeholder, value in mapping.items():
        if value is not None:
            result = result.replace(placeholder, value)
    # Remove escaped $$ markers.
    result = result.replace('$$', '$')
    return urljoin(base_url, result)


def _get_base_url(element: ElementTree.Element, inherited: str) -> str:
    base_url = inherited
    base_el = element.find('BaseURL')
    if base_el is not None and base_el.text:
        candidate = base_el.text.strip()
        if candidate:
            base_url = urljoin(inherited, candidate)
    return base_url

