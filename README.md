# VideoMaker – Automated TikTok Video Generator

VideoMaker is a fully automated, extensible system for generating, editing, and publishing short-form videos.
It supports multiple content sources (Reddit, YouTube, text splits), text-to-speech engines, video composition, audio mixing, and automated TikTok posting via Selenium.

The system is built in Python and orchestrates a full pipeline from content ingestion to final publishing.

---

## Features

### Content Builders

* **Reddit Stories Builder**

  * Fetches posts/comments using PRAW.
  * Translates (using `deep_translator`) and sanitizes text.
  * Generates narration via multiple TTS providers.
  * Creates vertical videos using YouTube clips as background.

* **Simple Splits Builder**

  * Downloads videos from YouTube playlists.
  * Detects highlight markers with the LemnosLife API.
  * Extracts interesting segments or fallback random chunks.
  * Creates split-screen videos with titles overlaid.

### Media Pipeline

* **Audio generation**

  * Google Cloud TTS
  * TTSMP3
  * gTTS
  * Auto speed-adjustment, gap insertion, and merging.

* **Video generation**

  * Background extraction and cropping (9:16 format).
  * Layering text, audio, and overlay clips.
  * Automatic subtitle line breaking.
  * Final rendering via MoviePy (H.265 codec).

### Automation & Persistence

* Reddit sampling history tracking.
* YouTube video usage tracking.
* Safe persistence of produced videos to avoid duplicates.
* Per-account generation settings.

### TikTok Auto-Posting

* Headless Chrome automation with cookie-based login.
* Multi-account support.
* Robust handling of upload screens and rendering delays.

---

## Project Structure

```
mastertuto-videomaker/
│
├── main.py                        # Orchestrates full run: generation + posting
├── requirements.txt
│
├── content/
│   ├── builders/                  # RedditStoriesBuilder, SimpleSplitsBuilder
│   ├── configs/                   # JSON profiles per channel/subreddit
│   ├── reddit/                    # Reddit fetching logic
│   ├── youtube/                   # YouTube playlist/handler tools
│   └── markers/                   # Detection of YouTube "most replayed" markers
│
├── media/
│   ├── audio/                     # TTS + audio mixing
│   ├── video/                     # VideoMaker (composition, overlays, rendering)
│   ├── text/                      # Text processing & layout
│   ├── stt/                       # Future speech-to-text subsystem
│   └── tts/                       # TTS providers (Google, gTTS, TTSMP3)
│
├── tiktok/                        # Automated posting
├── translate/                     # High-level translation interface
├── exceptions/
└── utilities/                     # Config, logging, persistence, helper functions
```

---

## Installation

### Requirements

* Python 3.10+
* Chrome installed
* A Google Cloud project (optional but recommended for TTS)
* YouTube API not required (Pytube only)
* Reddit API credentials for PRAW

### Install dependencies

```
pip install -r requirements.txt
```

---

## Configuration

### 1. Reddit API Credentials

Edit `utilities/config/reddit.py`:

```python
CLIENT_ID = "your_id"
CLIENT_SECRET = "your_secret"
```

### 2. TikTok Cookies

Generate and store cookies using browser extensions like **Cookie-Editor**, then place each account’s cookie file in your config folder.

### 3. Video Config Profiles

You can create infinite accounts in:

```
utilities/config/accounts.py
```

Each entry defines:

* Content type (`reddit_stories` or `simple_splits`)
* Source config file
* Voice language
* Cookie file path

Example:

```python
{
    "type": "reddit_stories",
    "lang": "pt-br",
    "login_file": "cookies/account1.json",
    "videos_config": ["askreddit_pt.json", "nosleep_pt.json"]
}
```

---

## Usage

Simply run:

```
python main.py
```

The system will:

1. Process pending videos from previous runs.
2. Shuffle accounts.
3. For each account:

   * Select two random video configs.
   * Build videos.
   * Save them.
   * Attempt to auto-post to TikTok.

All outputs are written under the configured `OUTPUT_FOLDER`.

---

## Adding New Content Types

You can extend the platform by implementing new builders:

```
content/builders/
```

Each builder must expose:

* `build(persistence, translate_to)`
* `deploy()`

---

## Developing CSS or Visual Layers

If you intend to add styling overlays, dynamic captions, or CSS-like layout rules, you may consider extending:

```
media/text/editor.py
media/video/maker.py
```

The repository is structured so that visual formatting logic is isolated from content sourcing.

---

## Roadmap

* Automatic caption generation (STT)
* Background music synchronization by BPM
* Template-based rendering
* OpenAI/GPT support for story rewriting
* Full web dashboard
