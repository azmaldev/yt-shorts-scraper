import logging
import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class ConfigModel(BaseModel):
    visitorData: str | None = Field(
        None, description="Extracted along with po token"
    )
    po_token: str | None = Field(
        None,
    )
    proxy: str | None = None
    cookiefile: str | None = None
    retries: int | None = 2
    quiet: bool | None = None
    verbose: bool | None = None
    geo_bypass: bool | None = True
    geo_bypass_country: str | None = None
    enable_logging: bool | None = False
    default_extension: str = "webm"
    default_audio_format: str = "m4a"
    working_directory: str = "static"
    frontend_dir: str | None = None
    serve_frontend_from_static_server: bool = False
    api_base_url: str | None = None

    @property
    def ytdlp_params(self) -> dict:
        params = {
            "cookiefile": self.cookiefile,
            "retries": self.retries,
            "verbose": self.verbose,
            "quiet": self.quiet,
            "geo_bypass": self.geo_bypass,
            "geo_bypass_country": self.geo_bypass_country,
            "keep_fragments": False,
            "fragment_retries": 2,
        }

        if self.proxy:
            params["proxy"] = self.proxy

        if self.enable_logging:
            params["logger"] = logging.getLogger("uvicorn")

        if self.quiet:
            logging.getLogger("yt_dlp_bonus").setLevel(logging.ERROR)
            logging.getLogger("yt_dlp").setLevel(logging.ERROR)

        if self.po_token:
            if self.cookiefile:
                params["extractor_args"] = {
                    "youtube": {
                        "player_client": ["web", "default"],
                        "po_token": [f"web+{self.po_token}"],
                    }
                }
            elif self.visitorData:
                params["extractor_args"] = {
                    "youtube": {
                        "player_client": ["web", "default"],
                        "player_skip": ["webpage", "configs"],
                        "po_token": [f"web+{self.po_token}"],
                        "visitor_data": [self.visitorData],
                    }
                }
        elif self.visitorData:
            params["extractor_args"] = {
                "youtube": {
                    "visitor_data": [self.visitorData],
                }
            }

        return params

    @field_validator("cookiefile")
    def validate_cookiefile(value):
        if not value:
            return
        cookiefile = Path(value)
        if not cookiefile.exists() or not cookiefile.is_file():
            raise ValueError(f"Invalid cookiefile passed - {value}")
        return value
