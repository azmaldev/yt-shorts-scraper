<div align="center">

# 🎬 YT Shorts Scraper

**Extract metadata, transcripts & audio from YouTube Shorts — instantly.**

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

A lightweight REST API that scrapes rich metadata from YouTube Shorts (videos ≤120s) and provides temporary audio downloads. Built on **FastAPI** with **yt-dlp** under the hood.

---

## 📦 What It Scrapes

| # | Field | Description | Example |
|---|-------|-------------|---------|
| 1 | `id` | YouTube video ID | `LaHO_FJq_b8` |
| 2 | `title` | Video title | `Joe Rogan Can't Believe What Mike Tyson Eats` |
| 3 | `channel` | Channel name | `Worthy Rogan` |
| 4 | `duration_string` | Duration in seconds | `17` |
| 5 | `thumbnail` | Thumbnail image URL | `https://i.ytimg.com/vi/.../sd2.jpg` |
| 6 | `like_count` | Number of likes | `62785` |
| 7 | `views_count` | Number of views | `1994503` |
| 8 | `hashtags` | Hashtags from description | `["#shorts"]` |
| 9 | `transcript` | Auto-generated English transcript | `"Mike Tyson's mind has switched..."` |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.14+**
- **Git**

### Setup

```sh
git clone https://github.com/azmaldev/yt-shorts-scraper.git
cd yt-shorts-scraper
pip install uv
uv venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
uv sync
```

### Run the server

```sh
uv run fastapi dev app
```

Open **http://localhost:8000/api/docs** for the interactive Swagger UI.

---

## 📡 API Endpoints

### `GET /api/metadata`

Returns all scraped metadata for a YouTube Shorts video.

**Input:** `url` — YouTube video URL or ID

```sh
curl "http://localhost:8000/api/metadata?url=https://youtube.com/shorts/LaHO_FJq_b8"
```

**Output:**

```json
{
  "id": "LaHO_FJq_b8",
  "title": "Joe Rogan Can't Believe What Mike Tyson Eats",
  "channel": "Worthy Rogan",
  "duration_string": "17",
  "thumbnail": "https://i.ytimg.com/vi/LaHO_FJq_b8/sd2.jpg",
  "like_count": 62785,
  "views_count": 1994503,
  "hashtags": [],
  "transcript": "Mike Tyson's mind has switched over into war..."
}
```

### `POST /api/download`

Downloads the audio track as a temporary m4a file.

**Input:** `url`, `quality` (`low` / `medium` / `high`)

```sh
curl -X POST "http://localhost:8000/api/download?url=https://youtube.com/shorts/LaHO_FJq_b8&quality=low" -o audio.m4a
```

---

## ⚙️ Configuration

Edit [`config.yml`](config.yml) to customize:

| Setting | Description |
|---------|-------------|
| `po_token` / `visitorData` | Browser auth tokens (avoids YouTube blocks) |
| `cookiefile` | Path to Netscape-format cookies file |
| `proxy` | HTTP/SOCKS proxy for requests |
| `retries` | Number of retry attempts (default: 3) |
| `default_extension` | `webm` or `mp4` |
| `default_audio_format` | `m4a` or `webm` |
| `geo_bypass` | Bypass geographic restrictions |
| `quiet` / `verbose` | Logging verbosity |

> 💡 Use `production.yml` as a tuned starting point for deployment.

---

## 🛠 Utility Servers

| Server | Purpose |
|--------|---------|
| [`servers/static.py`](servers/static.py) | Serves downloaded media files independently (reduces API load) |
| [`servers/proxy.py`](servers/proxy.py) | Forwards requests to a non-HTTPS API instance |

---

## 🔧 Troubleshooting

> **YouTube blocks your requests?**

YouTube actively flags requests without proper browser-like authorization.

**Solutions:**

1. **Cookies + PO Token** — Extract from your browser and set in `config.yml`.
   [Full guide →](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#po-token-guide)

2. **Whitelisted proxy** — Route through an IP that YouTube hasn't flagged.

3. **JS Runtime** — Install `deno` for better extraction:
   ```sh
   # Install deno, then yt-dlp will use it automatically
   ```

---

## 🏗 Project Structure

```
yt-shorts-scraper/
├── app/
│   ├── __init__.py        # FastAPI app entry point
│   ├── __main__.py        # CLI commands
│   ├── config.py          # Configuration loader
│   ├── models.py          # Pydantic models
│   ├── utils.py           # Helpers (URL parsing, error handling)
│   ├── v1/
│   │   ├── routes.py      # API routes (metadata + download)
│   │   ├── utils.py       # Extraction logic
│   │   └── models.py      # Response models
│   └── v2/                # Placeholder
├── servers/
│   ├── static.py           # Static file server
│   └── proxy.py            # HTTPS proxy server
├── tests/
│   ├── test_v1.py          # API tests
│   └── websocket_download.py
├── config.yml              # Configuration file
├── production.yml           # Production-ready config
└── pyproject.toml           # Project metadata & dependencies
```

---

## 📄 License

[MIT](LICENSE) — do whatever you want with it.
