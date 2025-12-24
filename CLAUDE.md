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
├── requirements.txt         # Python dependencies (gTTS, genanki, gspread, google-auth)
├── README.md                # User documentation
├── CLAUDE.md                # Technical documentation (this file)
├── GOOGLE_SHEETS_SETUP.md   # Google Sheets API setup guide
├── deck/                    # CSV files
│   ├── basic_fifty.csv
│   └── ...
├── audio/                   # Generated audio files (git-ignored)
├── output/                  # Generated Anki decks (.apkg files)
└── venv/                    # Virtual environment (git-ignored)
```

## Technical Details

### Dependencies
- Python 3.13
- `gTTS==2.5.3` - Text-to-speech
- `genanki==0.13.1` - Anki deck generation
- `gspread==6.1.4` - Google Sheets API integration
- `google-auth==2.36.0` - Google authentication

### CSV Format

**Standard Format (English → French):**
```csv
English,French
cat,chat
hello,bonjour
house,maison
```

**Reverse Format (French → English):**
```csv
French,English
chat,cat
bonjour,hello
maison,house
```

**Note**:
- Both columns are required
- The script detects column order by headers
- Reverse format creates cards with French on front, English on back
- Audio always pronounces the French text

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

1. **Deck ID Generation**: Uses MD5 hash of deck name to ensure unique deck IDs in Anki

2. **Column Order Detection**: Automatically detects if columns are swapped (French, English vs English, French)
   - CSV: Checks header row fieldnames
   - Google Sheets: Checks header cells from grid data
   - When swapped, values are remapped to show French on front, English on back
   - AudioText field tracks which text to use for pronunciation (always French)

3. **French Translation Required**: Validates that French translation is provided, skips entries without translation

4. **Audio Cleaning**: Processes text before generating audio with intelligent pausing
   - Strips text in parentheses: `(m)` removed from "chat (m)"
   - **Line break pauses**: Converts `<br>` to `. ` (period + space) to create natural pauses in speech
   - Removes other HTML tags: `<b>`, `<i>`, `<u>` etc. stripped from audio
   - Cleans up double periods and extra spaces
   - Preserves formatted text on card while speaking clean French with natural pauses

5. **Google Sheets Integration**: Uses service account authentication to read from Google Sheets API with formatting detection
   - **Bold Text Detection**: Automatically wraps bold text from Google Sheets with `<b></b>` tags
   - Supports both entire cell bold and mixed formatting (some text bold, some not)
   - Uses `fetch_sheet_metadata` with `includeGridData=True` to access formatting information
   - **Newline Conversion**: Automatically converts newlines in Google Sheets cells to `<br>` tags
   - Users can press Alt+Enter (Cmd+Enter on Mac) to create multiline text, Ctrl+B to make text bold
   - All formatting is converted to HTML for proper display in Anki

6. **Intelligent Caching**: Hashes sheet content and skips regenerating unchanged decks
   - Cache stored in `.sheet_cache.json`
   - Checks content hash and output file existence before processing
   - Significantly improves performance on repeated runs

7. **Multi-Sheet Processing**: By default, processes ALL sheets in a spreadsheet, generating separate decks for each

8. **Dual Input Support**: Main function detects input type (CSV vs Sheets) and loads accordingly

9. **Deck Naming**: Converts filename or sheet name to title case for deck names

10. **Audio Files**: Named using MD5 hash of English word to avoid special characters

11. **Randomization**: Shuffles word order before processing to randomize flashcard order

## Recent Changes

### December 2025
- **2025-12-23**: Removed image generation feature and Pexels API integration
- **2025-12-23**: Removed `requests` dependency (no longer needed)
- **2025-12-23**: Removed Image column support from CSV and Google Sheets modes
- **2025-12-23**: Updated documentation to clarify two modes (CSV and Google Sheets)

### October 2025
- **2025-10-27**: Added reverse mode - supports `French,English` column order for French→English cards
- **2025-10-27**: Line breaks (`<br>`) converted to periods in audio for natural pauses between lines
- **2025-10-27**: Google Sheets bold formatting automatically wraps with `<b></b>` tags
- **2025-10-27**: Google Sheets newlines automatically convert to `<br>` tags for Anki display
- **2025-10-27**: Added HTML tag stripping from audio (supports `<b>`, `<i>`, `<u>` in cards)
- **2025-10-27**: Removed automatic translation - French translations must now be provided
- **2025-10-27**: Removed `deep-translator` dependency
- **2025-10-27**: Added intelligent caching - skips regenerating decks for unchanged sheets
- **2025-10-27**: Google Sheets now processes ALL sheets by default - generates separate deck for each sheet
- **2025-10-27**: Added Google Sheets integration - can now load vocabulary from online spreadsheets
- **2025-10-27**: Added flashcard randomization - order shuffled each time you generate
- **2025-10-12**: Changed CSV format to `English,French` columns; removed article detection
- **2025-10-12**: Fixed duplicate deck issue by generating unique deck IDs from deck names

## Configuration (config.py)
- `AUDIO_DIR = "audio"` - Audio output directory
- `OUTPUT_DIR = "output"` - Deck/CSV output directory
- `TTS_LANGUAGE = "fr"` - French language code
- `TTS_SLOW = False` - Normal speed pronunciation
- `GOOGLE_CREDENTIALS_FILE = "credentials.json"` - Path to Google service account credentials
- `SHEET_CACHE_FILE = ".sheet_cache.json"` - Cache file for tracking sheet changes

## Setup
- See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for complete instructions on setting up Google Sheets API access
