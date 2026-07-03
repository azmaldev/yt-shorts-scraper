import logging
import re
import typing as t
from functools import wraps

from fastapi import HTTPException, status
from yt_dlp.utils import DownloadError
from yt_dlp_bonus.exceptions import (
    FileSizeOutOfRange,
    UknownDownloadFailure,
    UserInputError,
)

from app.exceptions import InvalidVideoUrl

logger = logging.getLogger(__file__)

compiled_video_id_patterns = (
    re.compile(r"^https?://youtu\.be/([\w\-_]{11}).*"),
    re.compile(r"^https?://www\.youtube\.com/watch\?v=([\w\-_]{11})$"),
    re.compile(r"^https?://www\.youtube\.com/embed/([\w\-_]{11})$"),
    re.compile(r"^([\w\-_]{11})$"),
    re.compile(r"^https?://youtube\.com/shorts/([\w\-_]{11}).*"),
    re.compile(r"^https?://www\.youtube\.com/shorts/([\w\-_]{11})$"),
)

compiled_ytdlp_download_error_msg_pattern = re.compile(
    r".*\s[\w\-_]{11}:\s+(Video\s+.+)"
)


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|#]', "", filename)
    return cleaned.strip()


def router_exception_handler(func: t.Callable):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except HTTPException as e:
            raise e
        except (
            AssertionError,
            UserInputError,
            InvalidVideoUrl,
            FileSizeOutOfRange,
            UknownDownloadFailure,
        ) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )
        except DownloadError as e:
            msg = re.findall(compiled_ytdlp_download_error_msg_pattern, e.msg)
            if msg:
                detail = msg[0]
                status_code = status.HTTP_403_FORBIDDEN
            else:
                detail = (
                    "Server encountered an issue while trying to handle that"
                    " request!"
                )
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code, detail)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server encountered an issue while trying to handle that request!",
            )

    return decorator


def get_video_id(url: str) -> str:
    for compiled_pattern in compiled_video_id_patterns:
        match = compiled_pattern.match(url)
        if match:
            return match.group(1)
    raise InvalidVideoUrl(f"Invalid video url passed - {url}")
