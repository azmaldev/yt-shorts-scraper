import pytest

import app.v1.models as models
from tests import client


@pytest.mark.parametrize(
    ["url"],
    [
        ("https://youtu.be/HUGcwe93F9E?si=Ajunj8GlRs-DzKnQ",),
        ("HUGcwe93F9E",),
        ("https://www.youtube.com/watch?v=HUGcwe93F9E",),
    ],
)
def test_video_metadata(url):
    resp = client.get("/api/metadata", params=dict(url=url))
    assert resp.is_success
    models.MetadataResponse(**resp.json())


@pytest.mark.parametrize(
    ["url", "quality"],
    [
        ("https://youtu.be/S3wsCRJVUyg?si=SjN17MR1-u7BPgxk", "low"),
        ("https://youtu.be/S3wsCRJVUyg?si=SjN17MR1-u7BPgxk", "medium"),
    ],
)
def test_download_audio_temp(url, quality):
    resp = client.post("/api/download", params=dict(url=url, quality=quality))
    if not resp.is_success:
        print(resp.text)
    assert resp.is_success
    assert "audio" in resp.headers.get("content-type", "")
