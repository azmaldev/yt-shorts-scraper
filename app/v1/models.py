from pydantic import BaseModel, Field, HttpUrl


class MetadataResponse(BaseModel):
    id: str
    title: str
    channel: str | None = None
    duration_string: str | None = None
    thumbnail: HttpUrl | None = None
    like_count: int | None = None
    views_count: int | None = None
    hashtags: list[str] = Field(default_factory=list, description="Hashtags extracted from description")
    transcript: str | None = Field(None, description="Auto-generated English transcript text")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "HbmyBac3vjk",
                "title": "AI voice cloned calling system for real estate agents.",
                "channel": "Jess's AI Agents Hub",
                "duration_string": "1:10",
                "thumbnail": "https://i.ytimg.com/vi/HbmyBac3vjk/maxresdefault.jpg",
                "like_count": 2777,
                "views_count": 114024,
                "hashtags": ["#shorts", "#aitools"],
                "transcript": "So today I'm going to show you how to build an AI voice..."
            }
        }
    }
