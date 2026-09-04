# Telegram Media Bot

Telegram bot for downloading media from supported URLs with `yt-dlp` and sending the file back to the chat.

## What It Does

The bot listens for a URL, checks whether `yt-dlp` can process it, downloads the media into a local folder, and sends the resulting file back to Telegram.

Current flow:

1. User opens the bot and sends `/start`.
2. The bot shows inline buttons.
3. The user taps `Send URL`.
4. The user pastes a supported media URL.
5. The bot validates the URL, checks file size, downloads the file, and sends it back.

## Features

- `/start` command with inline buttons for the main action path
- URL validation through `yt-dlp`
- Download size limit enforcement before downloading
- Local download storage with cleanup after sending
- Support for both pip and conda based environments

## Requirements

- Python 3.12+
- A Telegram bot token from BotFather
- `yt-dlp` access to the media source you want to download from

## Files Involved

- `bot/main.py` starts the application and registers handlers
- `bot/command_registry.py` wires commands, callback queries, and text handlers
- `bot/handler/start.py` sends the welcome message and inline keyboard
- `bot/handler/url_handler.py` validates URLs and hands valid input to the download flow
- `bot/handler/download.py` checks file size, downloads media, sends the file, and deletes it afterward
- `bot/config.py` loads environment variables and default settings

## Configuration

Set these environment variables before running the bot:

- `BOT_TOKEN`: required Telegram bot token
- `DOWNLOAD_DIR`: directory used for downloaded files, defaults to `./downloads`
- `MAX_FILE_SIZE_MB`: maximum allowed file size in megabytes, defaults to `100`
- `DEFAULT_YT_DLP_FORMAT`: default yt-dlp format, defaults to `bestaudio/best`
- `LOG_LEVEL`: logging level, defaults to `INFO`

If you use a `.env` file, the bot loads it automatically through `python-dotenv`.

Example `.env` file:

```env
BOT_TOKEN=123456:example-token
DOWNLOAD_DIR=./downloads
MAX_FILE_SIZE_MB=100
DEFAULT_YT_DLP_FORMAT=bestaudio/best
LOG_LEVEL=INFO
```

## Installation

### Conda

```bash
conda env create -f environment.yml
conda activate telegram-installer
python -m pip install --upgrade pip
```

### Pip

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you are using conda, the repository already includes `environment.yml`. If you are using venv, install the dependencies from `requirements.txt`.

## Run

```bash
python bot/main.py
```

The entrypoint is written so it works when launched from the repository root with the command above.

## Usage

1. Start the bot in Telegram using `/start`.
2. Tap `Send URL`.
3. Send a media URL that `yt-dlp` supports.
4. Wait for the status messages while the bot checks and downloads the file.
5. Receive the file in the chat when the download completes.

If the URL is invalid or unsupported, the bot replies with an error message and waits for another URL.

If the file is larger than `MAX_FILE_SIZE_MB`, the bot stops before downloading and tells you the limit was exceeded.

## Development Notes

- Downloads are stored locally and removed after the file is sent.
- The current code uses a simple callback query flow for the `Send URL` button.
- Text messages are treated as candidate URLs only after the bot has asked for one.
- The project currently does not include an automated test suite.

## How It Works

1. The start handler sends a welcome message with inline buttons.
2. The callback handler marks the chat as waiting for a URL.
3. The message handler validates the input with `yt-dlp`.
4. The download handler checks the size limit, downloads the media, sends the file, and removes the local copy.

## Project Layout

```text
bot/
  main.py
  config.py
  command_registry.py
  handler/
    start.py
    url_handler.py
    download.py
  keyboards/
  services/
  utils/
tests/
```

## Notes

- The current entrypoint is `python bot/main.py`.
- The bot expects `BOT_TOKEN` to be present before startup.
- The download directory is created automatically if it does not exist.

## Troubleshooting

- If you see `ModuleNotFoundError: No module named 'telegram'`, install the dependencies in the active environment.
- If the bot exits with `BOT_TOKEN is required in environment`, set the token in your shell or `.env` file.
- If `yt-dlp` rejects a URL, the bot will not start a download and will ask for another link.