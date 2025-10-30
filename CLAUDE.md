# Claude Code Context

## Project Overview
French Flashcard Generator - A Python tool that generates audio pronunciation using Google Text-to-Speech and creates Anki flashcard decks from English-French vocabulary pairs.

## Key Features
- Requires French translations to be provided (no automatic translation)
- Generates MP3 audio files with pronunciation for all entries
- Creates importable Anki deck files (.apkg)
- Google Sheets integration - load vocabulary from online spreadsheets
- Supports both local CSV files and cloud-based Google Sheets
- Randomizes flashcard order each time you generate a deck
- Intelligent caching - skips regenerating unchanged sheets
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
- `gTTS==2.5.3` - Text-to-speech
- `genanki==0.13.1` - Anki deck generation
- `gspread==6.1.4` - Google Sheets API integration
- `google-auth==2.36.0` - Google authentication

### CSV Format
```csv
English,French
cat,chat
hello,bonjour
house,maison
table,une table
```

**Note**: Both English and French columns are required. Rows without French translations will be skipped.

### Usage
```bash
# Activate virtual environment
source venv/bin/activate

# CSV mode: Run with specific file
python french_flashcards.py deck/basic_fifty.csv

# Google Sheets mode: Generate from ALL sheets in spreadsheet
python french_flashcards.py -s SPREADSHEET_ID

# Google Sheets mode: Generate from only one specific sheet
python french_flashcards.py -s SPREADSHEET_ID -n "Calendar"
```

### Key Implementation Details
1. **Deck ID Generation**: Uses MD5 hash of deck name to ensure unique deck IDs in Anki (french_flashcards.py:47)
2. **French Translation Required**: Validates that French translation is provided, skips entries without translation (french_flashcards.py:56-66)
3. **Audio Cleaning**: Removes parenthetical text and HTML tags before generating audio (french_flashcards.py:68-84)
   - Strips text in parentheses: `(m)` removed from "chat (m)"
   - Strips HTML tags: `<br>`, `<b>`, `<i>` etc. removed from audio
   - Preserves formatted text on card while speaking clean French
4. **Google Sheets Integration**: Uses service account authentication to read from Google Sheets API (french_flashcards.py:171-240)
5. **Intelligent Caching**: Hashes sheet content and skips regenerating unchanged decks (french_flashcards.py:243-294)
   - Cache stored in `.sheet_cache.json`
   - Checks content hash and output file existence before processing
   - Significantly improves performance on repeated runs
6. **Multi-Sheet Processing**: By default, processes ALL sheets in a spreadsheet, generating separate decks for each (french_flashcards.py:330-397)
7. **Sheet Discovery**: Automatically fetches all sheet names from spreadsheet (french_flashcards.py:195-207)
8. **Dual Input Support**: Main function detects input type (CSV vs Sheets) and loads accordingly (french_flashcards.py:301-434)
9. **Deck Naming**: Converts filename or sheet name to title case for deck names (french_flashcards.py:290-298)
10. **Audio Files**: Named using MD5 hash of English word to avoid special characters (french_flashcards.py:117)
11. **Randomization**: Shuffles word order before processing to randomize flashcard order (french_flashcards.py:360, 416)

## Recent Changes
- **2025-10-27**: Added HTML tag stripping from audio (supports `<br>`, `<b>`, `<i>`, etc. in cards)
- **2025-10-27**: Removed automatic translation - French translations must now be provided
- **2025-10-27**: Removed `deep-translator` dependency (no longer needed)
- **2025-10-27**: Removed `-t` flag and `translate_csv` function (translation mode)
- **2025-10-27**: Added intelligent caching - skips regenerating decks for unchanged sheets
- **2025-10-27**: Output filenames from Google Sheets now preserve original case (spaces → underscores)
- **2025-10-27**: Google Sheets now processes ALL sheets by default - generates separate deck for each sheet
- **2025-10-27**: Added Google Sheets integration - can now load vocabulary from online spreadsheets
- **2025-10-27**: Added flashcard randomization - order shuffled each time you generate
- **2025-10-12**: Changed CSV format to `English,French` columns; removed article detection
- Fixed duplicate deck issue by generating unique deck IDs from deck names
- Made input file a command-line argument

## Configuration (config.py)
- `AUDIO_DIR = "audio"` - Audio output directory
- `OUTPUT_DIR = "output"` - Deck/CSV output directory
- `TTS_LANGUAGE = "fr"` - French language code
- `TTS_SLOW = False` - Normal speed pronunciation
- `GOOGLE_CREDENTIALS_FILE = "credentials.json"` - Path to Google service account credentials
- `SHEET_CACHE_FILE = ".sheet_cache.json"` - Cache file for tracking sheet changes

## Setup
- See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for complete instructions on setting up Google Sheets API access
