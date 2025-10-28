# French Flashcard Generator

A Python tool that generates Anki flashcards for learning French vocabulary. It can auto-translate English words/phrases to French or use your provided translations, and generates audio pronunciation files for all entries.

## Features

- 🔄 Translates English words/phrases to French using Google Translate (or use your own translations)
- 🔊 Generates audio pronunciation files using Google Text-to-Speech
- 📇 Creates Anki flashcard decks (.apkg) ready to import
- ✏️ Supports pre-filled French translations or automatic lookup
- 🎯 Two-step workflow: translate first, then generate cards
- ☁️ **NEW**: Google Sheets support - edit vocabulary lists online from anywhere!

## Installation

### 1. Set Up Virtual Environment

Create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when the virtual environment is active.

### 2. Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

### 3. Deactivate Virtual Environment

When you're done working on the project:

```bash
deactivate
```

This returns you to your system's default Python environment.

## Creating a Deck: Complete Workflow

### Step 1: Create Your CSV File

Create a CSV file with two columns: `English` and `French`

```csv
English,French
hello,
goodbye,
cat,
dog,
thank you,
```

- **English column** (required): The English word or phrase
- **French column** (optional): Leave empty for auto-translation, or provide your own

Save this file (e.g., `deck/my_words.csv`)

### Step 2: Activate Virtual Environment

```bash
# Navigate to the project directory
cd /path/to/french-flash

# Activate the virtual environment
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3: Translate Missing Words

Run the script with the `-t` flag to translate any empty French fields:

```bash
python french_flashcards.py -t deck/my_words.csv
```

This will:
- Translate all empty French entries
- Update the CSV file with the translations
- Show you what was translated

### Step 4: Review and Edit Translations (Optional)

Open `deck/my_words.csv` and review the auto-generated translations. You can edit any that need correction.

### Step 5: Generate the Anki Deck

Run the script without the `-t` flag to create the flashcard deck:

```bash
python french_flashcards.py deck/my_words.csv
```

This will:
- Generate audio pronunciation files for all French words/phrases
- Create an Anki deck file at `output/my_words.apkg`
- Note: Text in parentheses is kept on the card but not included in audio

### Step 6: Import into Anki

1. Open Anki
2. Click "File" → "Import"
3. Select `output/my_words.apkg`
4. Click "Import"

Your French flashcards are now ready to study!

### Step 7: Deactivate Virtual Environment

When finished:

```bash
deactivate
```

## Quick Reference

### CSV Files (Local)

```bash
# Activate virtual environment
source venv/bin/activate

# Translate empty French entries (updates CSV)
python french_flashcards.py -t deck/my_words.csv

# Generate flashcard deck from CSV
python french_flashcards.py deck/my_words.csv

# Show help
python french_flashcards.py --help

# Deactivate virtual environment when done
deactivate
```

### Google Sheets (Online)

```bash
# Activate virtual environment
source venv/bin/activate

# Generate flashcard decks from ALL sheets in spreadsheet
python french_flashcards.py -s YOUR_SPREADSHEET_ID

# Generate from only a specific sheet
python french_flashcards.py -s YOUR_SPREADSHEET_ID -n "Calendar"

# Deactivate virtual environment when done
deactivate
```

**Note**: By default, the script processes **all sheets** in your spreadsheet and generates a separate deck for each one!

**📖 [Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)** - Complete instructions for setting up Google Sheets API access

## Output Files

The script generates:

- `output/<deck_name>.apkg` - Anki deck file (ready to import)
- `audio/*.mp3` - Audio pronunciation files (automatically included in .apkg)

## Configuration

Edit `config.py` to customize:

- `TTS_SLOW` - Set to `True` for slower pronunciation (useful for beginners)
- Directory paths
- Language settings

## Project Structure

```
french-flash/
├── french_flashcards.py    # Main script
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── deck/                    # Your CSV files
│   ├── a_year.csv           # Example: days, months, seasons
│   ├── basic_fifty.csv      # Example: 50 common words
│   ├── basic_french.csv     # Example: basic vocabulary
│   └── perfect_one.csv      # Example: rooms in a house
├── audio/                   # Generated audio files
├── output/                  # Generated Anki decks (.apkg)
└── venv/                    # Virtual environment (created during setup)
```

## Requirements

- Python 3.13 or compatible version
- Internet connection (for translation and TTS)

## Notes

- ⚠️ Always activate the virtual environment before running the script
- 🌐 Requires an internet connection for translation (when needed) and text-to-speech
- 📝 Text in parentheses (e.g., "chat (m)") appears on cards but is excluded from audio
- ✏️ You can manually edit translations in the CSV after running `-t` flag
- 🔊 Audio files are automatically embedded in the .apkg file
- ☁️ Google Sheets mode requires API setup (see [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md))
- 🔀 Flashcards are randomized each time you generate a deck

## License

MIT
