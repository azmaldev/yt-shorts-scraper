import json
import re

import requests
import yt_dlp
from yt_dlp_bonus import YoutubeDLBonus
from yt_dlp_bonus.models import ExtractedInfo


def get_extracted_info(yt: YoutubeDLBonus, url: str) -> ExtractedInfo:
    return yt.extract_info_and_form_model(url)


def extract_hashtags(extracted_info: ExtractedInfo) -> list[str]:
    description = extracted_info.description or ""
    return re.findall(r"#\w+", description)


def extract_transcript(video_id: str) -> str | None:
    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"https://www.youtube.com/watch?v={video_id}", download=False
        )
        captions = info.get("automatic_captions") or {}
        en_captions = captions.get("en") or []
        if not en_captions:
            return None
        json3_url = None
        for c in en_captions:
            if c.get("ext") == "json3":
                json3_url = c.get("url")
                break
        if not json3_url:
            json3_url = en_captions[0].get("url")
        if not json3_url:
            return None
        resp = requests.get(json3_url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        events = data.get("events", [])
        text_parts = []
        for event in events:
            segs = event.get("segs", [])
            for seg in segs:
                utf8 = seg.get("utf8", "")
                text_parts.append(utf8)
        return " ".join(text_parts).strip() or None
