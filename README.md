# EcoTrace AI

EcoTrace AI is a Telegram nature guide for people who are already outdoors. Describe
something you found or send a photo, get a cautious identification with practical
safety advice, and get back to exploring. It can help with plants, animals, tracks,
and other nature observations.

## Touch Grass challenge

The goal is to make the screen the shortest part of a nature encounter: ask a
question or take a photo, read a concise field guide, then put the phone away.
EcoTrace AI supports both quick text descriptions and photo-based observations.
It asks the model to explain uncertainty, avoid unsupported species-level claims,
and never suggest touching or eating an unfamiliar wild organism.

### Why open AI

The core inference runs locally through [Ollama](https://ollama.com/) using
open-weight models. For a photo, Moondream describes visible details and Gemma
uses that description and the user's question to produce the guide. For text-only
questions, Gemma responds directly. The default text model is `gemma2:2b`, and
the model can be changed with the `DEFAULT_MODEL` environment variable.

Running inference on a machine you control means the image and prompt are sent
to the local model runtime rather than an external AI inference API. The open
model setup also makes it possible to swap models and change the instructions
that shape the guide. The Telegram bot still needs an internet connection to
receive and send messages, so EcoTrace AI is not an end-to-end offline trail app.
If configured, Sentry also receives telemetry for tracing and error reporting.

## How it works

1. Start a chat with the bot and choose Photo ID or Text ID.
2. Send a photo with an optional question, or describe what you found. Adding
   location and visible details can help.
3. For photos, Moondream reports visual features without naming the subject;
   Gemma then generates a likely identification and safety advice.
4. Review the uncertainty and safety guidance, then continue observing outdoors.

The bot temporarily downloads photos for analysis and removes the local image
file afterwards. Messages are still handled by Telegram, and optional Sentry
telemetry is sent to the configured Sentry project.

## Requirements

- Python and pip
- [Ollama](https://ollama.com/) installed and running
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- The Ollama models `gemma2:2b` and `moondream`

## Run locally

1. Clone this repository and enter its directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Ollama is running and download the models:

   ```bash
   ollama pull gemma2:2b
   ollama pull moondream
   ```

5. Create a `.env` file in the project root:

   ```dotenv
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   DEFAULT_MODEL=gemma2:2b
   # Optional: enable Sentry tracing and error reporting
   SENTRY_DSN=
   ```

6. Start the bot:

   ```bash
   python main.py
   ```

Open your bot in Telegram and send `/start`.

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Yes | Connects the bot to Telegram. |
| `DEFAULT_MODEL` | No | Ollama model used for the text guide; defaults to `gemma2:2b`. |
| `SENTRY_DSN` | No | Enables Sentry tracing and error reporting when set. |

The photo workflow currently uses `moondream` for image description and then
`DEFAULT_MODEL` for the final answer.

## Safety and limitations

AI identifications can be wrong. Treat them as suggestions, not authoritative
identifications. Do not touch or consume an unfamiliar wild plant or animal;
seek help from a qualified local expert if safety is uncertain. Photo analysis
depends on the visible details in the image, and the bot does not currently
provide live web research or location-based species lookup.

## Event submission

This project is built for the **Touch Grass** theme and uses open-weight Gemma
as its core text model, with local Ollama inference and a local vision-model step.
For a DEV submission, include a demo and what happened during an outdoor test;
no field-test results or demo link are claimed here.

Suggested challenge tags: `#devchallenge` `#hf26challenge`
