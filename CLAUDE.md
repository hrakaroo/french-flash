# Claude Code Context

## Project Overview
French Flashcard Generator - A Python tool that translates English words to French, generates audio pronunciation using Google Text-to-Speech, and creates Anki flashcard decks.

## Key Features
- Translates English → French using Google Translate API (or uses provided translations)
- Supports pre-filled French translations or automatic lookup
- Generates MP3 audio files with pronunciation for all entries
- Creates importable Anki deck files (.apkg)
- **NEW**: Google Sheets integration - load vocabulary from online spreadsheets
- Supports both local CSV files and cloud-based Google Sheets
- Randomizes flashcard order each time you generate a deck
- Deck names derived from input CSV filename or sheet name

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
- `gspread==6.1.4` - Google Sheets API integration
- `google-auth==2.36.0` - Google authentication

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

# CSV mode: Run with specific file
python french_flashcards.py deck/basic_fifty.csv

# CSV mode: Translate missing entries
python french_flashcards.py -t deck/basic_fifty.csv

# Google Sheets mode: Generate from ALL sheets in spreadsheet
python french_flashcards.py -s SPREADSHEET_ID

# Google Sheets mode: Generate from only one specific sheet
python french_flashcards.py -s SPREADSHEET_ID -n "Calendar"
```

### Key Implementation Details
1. **Deck ID Generation**: Uses MD5 hash of deck name to ensure unique deck IDs in Anki (french_flashcards.py:47)
2. **Translation Logic**: Uses provided French translation if available, otherwise calls Google Translate (french_flashcards.py:54-71)
3. **Google Sheets Integration**: Uses service account authentication to read from Google Sheets API (french_flashcards.py:171-240)
4. **Multi-Sheet Processing**: By default, processes ALL sheets in a spreadsheet, generating separate decks for each (french_flashcards.py:354-401)
5. **Sheet Discovery**: Automatically fetches all sheet names from spreadsheet (french_flashcards.py:195-207)
6. **Dual Input Support**: Main function detects input type (CSV vs Sheets) and loads accordingly (french_flashcards.py:336-444)
7. **Deck Naming**: Converts filename or sheet name to title case for deck names (french_flashcards.py:242-248)
8. **Audio Files**: Named using MD5 hash of English word to avoid special characters (french_flashcards.py:120)
9. **Randomization**: Shuffles word order before processing to randomize flashcard order (french_flashcards.py:381, 422)

## Recent Changes
- **2025-10-27**: Output filenames from Google Sheets now preserve original case (spaces → underscores)
- **2025-10-27**: Google Sheets now processes ALL sheets by default - generates separate deck for each sheet
- **2025-10-27**: Added Google Sheets integration - can now load vocabulary from online spreadsheets
- **2025-10-27**: Added flashcard randomization - order shuffled each time you generate
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
- `GOOGLE_CREDENTIALS_FILE = "credentials.json"` - Path to Google service account credentials

## Setup
- See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for complete instructions on setting up Google Sheets API access
