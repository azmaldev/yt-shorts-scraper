import os
import tempfile
from pathlib import Path

import shutil

from fastapi import APIRouter, HTTPException, Query, status
from starlette.background import BackgroundTask
from fastapi.responses import FileResponse
from yt_dlp_bonus import Downloader, YoutubeDLBonus
from yt_dlp_bonus.constants import audioQualities

from app.config import loaded_config
from app.utils import get_video_id, router_exception_handler, sanitize_filename
from app.v1.models import MetadataResponse
from app.v1.utils import extract_hashtags, extract_transcript, get_extracted_info

router = APIRouter()

yt = YoutubeDLBonus(params=loaded_config.ytdlp_params)

downloader = Downloader(
    yt=yt,
    working_directory=Path(tempfile.gettempdir()),
    clear_temps=True,
)


def is_short_or_raise(extracted_info) -> None:
    duration = extracted_info.duration or 0
    if duration > 120:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Video is {duration}s long — only videos ≤120s (Shorts) are "
                "accepted."
            ),
        )


@router.get("/metadata", name="Video metadata")
@router_exception_handler
def get_video_metadata(
    url: str = Query(description="YouTube video URL or ID"),
) -> MetadataResponse:
    extracted_info = get_extracted_info(yt=yt, url=url)
    is_short_or_raise(extracted_info)

    video_id = get_video_id(url)
    hashtags = extract_hashtags(extracted_info)
    transcript = extract_transcript(video_id)

    return MetadataResponse(
        id=extracted_info.id,
        title=extracted_info.title,
        channel=extracted_info.channel,
        duration_string=extracted_info.duration_string,
        thumbnail=extracted_info.thumbnail,
        like_count=extracted_info.like_count,
        views_count=extracted_info.view_count,
        hashtags=hashtags,
        transcript=transcript,
    )


@router.post("/download", name="Extract audio (temp)")
@router_exception_handler
def download_audio_temp(
    url: str = Query(description="YouTube video URL or ID"),
    quality: str = Query("low", description="Audio quality"),
):
    extracted_info = get_extracted_info(yt=yt, url=url)
    is_short_or_raise(extracted_info)

    target_format = None
    if quality in audioQualities:
        video_formats = yt.get_video_qualities_with_extension(
            extracted_info,
            ext=loaded_config.default_extension,
            audio_ext=loaded_config.default_audio_format,
        )
        target_format = video_formats.get(quality)
        if not target_format:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Audio quality '{quality}' not available.",
            )

    tmpdir = tempfile.mkdtemp()
    processed = downloader.ydl_run_audio(
        extracted_info,
        audio_format=target_format.format_id if target_format else None,
        bitrate=None,
        ytdl_params={
            "outtmpl": os.path.join(
                tmpdir,
                f"{sanitize_filename(extracted_info.title)}.%(ext)s",
            )
        },
    )
    filepath = Path(processed["requested_downloads"][0]["filepath"])

    def cleanup():
        shutil.rmtree(tmpdir, ignore_errors=True)

    return FileResponse(
        path=filepath,
        filename=filepath.name,
        media_type="audio/m4a",
        background=BackgroundTask(cleanup),
    )
