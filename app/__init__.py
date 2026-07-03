"""YouTube Shorts metadata + temp audio extraction microservice."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import pyproject_dot_toml_details

project_details = pyproject_dot_toml_details["project"]

from app.v1 import v1_router  # noqa: E402

app = FastAPI(
    title="YouTube Shorts Microservice",
    version=project_details["version"],
    summary=project_details["description"],
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(v1_router, prefix="/api", tags=["v1"])


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/api/docs")
