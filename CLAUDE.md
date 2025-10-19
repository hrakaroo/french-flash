# Claude Code Context

## Project Overview
French Flashcard Generator - A Python tool that translates English words to French, generates audio pronunciation using Google Text-to-Speech, and creates Anki flashcard decks.

## Key Features
- Translates English → French using Google Translate API (or uses provided translations)
- Supports pre-filled French translations or automatic lookup
- Generates MP3 audio files with pronunciation for all entries
- Creates importable Anki deck files (.apkg)
- Exports vocabulary to CSV
- Deck names derived from input CSV filename

## Project Structure
```
french-flash/
├── french_flashcards.py    # Main script
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies (deep-translator, gTTS, genanki)
├── example_words.csv        # Example word list
├── basic_fifty.csv          # 50 common French words
├── audio/                   # Generated audio files (git-ignored)
├── output/                  # Generated Anki decks and CSV files
├── venv/                    # Virtual environment (git-ignored)
└── README.md                # Documentation
```

## Technical Details

### Dependencies
- Python 3.13
- `deep-translator==1.11.4` - Translation (compatible with Python 3.13, replaces googletrans)
- `gTTS==2.5.3` - Text-to-speech
- `genanki==0.13.1` - Anki deck generation

### CSV Format
```csv
English,French
cat,           # Leave empty for auto-translation
hello,bonjour  # Provide translation to skip lookup
house,         # Auto-translate
table,une table # Use your own translation
```

### Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run with specific file
python french_flashcards.py basic_fifty.csv

# Run with default (basic_french.csv or first available)
python french_flashcards.py
```

### Key Implementation Details
1. **Deck ID Generation**: Uses MD5 hash of deck name to ensure unique deck IDs in Anki (french_flashcards.py:45)
2. **Translation Logic**: Uses provided French translation if available, otherwise calls Google Translate (french_flashcards.py:52-68)
3. **Deck Naming**: Converts filename (e.g., `basic_fifty.csv` → "Basic Fifty") (french_flashcards.py:182-188)
4. **Audio Files**: Named using MD5 hash of English word to avoid special characters (french_flashcards.py:115)

## Recent Changes
- **2025-10-12**: Changed CSV format to `English,French` columns; removed article detection; French column is optional
- Updated from `googletrans` to `deep-translator` for Python 3.13 compatibility
- Fixed duplicate deck issue by generating unique deck IDs from deck names
- Made input file a command-line argument
- Converted all existing CSV files to new format

## Configuration (config.py)
- `AUDIO_DIR = "audio"` - Audio output directory
- `OUTPUT_DIR = "output"` - Deck/CSV output directory
- `TTS_LANGUAGE = "fr"` - French language code
- `TTS_SLOW = False` - Normal speed pronunciation
- `SOURCE_LANG = "en"` - English input
- `TARGET_LANG = "fr"` - French output
