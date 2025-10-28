"""Configuration settings for French flashcard generator."""

import os

# Directories
AUDIO_DIR = "audio"
OUTPUT_DIR = "output"

# Ensure directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Google Text-to-Speech settings
TTS_LANGUAGE = "fr"
TTS_SLOW = False  # Set to True for slower pronunciation

# Translation settings
SOURCE_LANG = "en"
TARGET_LANG = "fr"

# Google Sheets settings
GOOGLE_CREDENTIALS_FILE = "credentials.json"  # Path to your Google service account credentials
