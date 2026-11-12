# Astra — Python Voice Assistant

A compact personal assistant built with Python. Text mode works with the Python standard library; optional speech packages add microphone input and spoken replies.

## Features

- Text command interface; no API key required
- Optional speech recognition and text-to-speech
- Date and local time responses
- Safe arithmetic calculator using a restricted Python AST (never `eval`)
- Save and read notes in a local text file
- Unit tests for commands, note storage, and calculator safety

## Requirements

Python 3.10 or newer.

## Run in text mode

```bash
python assistant.py
```

Type `help` to see commands. Examples: `hello`, `time`, `date`, `calculate 12 * (3 + 2)`, `note revise Python functions`, and `read notes`. Type `exit` to quit.

## Enable voice mode

Install optional dependencies:

```bash
python -m pip install -r requirements-voice.txt
python assistant.py --voice
```

Voice recognition uses the SpeechRecognition package's Google Web Speech recognizer, which requires a microphone and internet access. PyAudio installation differs by operating system; install the appropriate audio backend if pip cannot provide it.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
ai-voice-assistant/
├── assistant.py
├── requirements-voice.txt
├── tests/test_assistant.py
├── .github/workflows/tests.yml
└── README.md
```

## Scope and future improvements

This version is a command-based assistant, not a general-purpose AI chatbot and does not claim Claude/OpenAI API integration. Future extensions could add a configurable LLM provider, wake-word detection, multilingual support, and a desktop UI.

No software license has been added; all rights are reserved by default.
