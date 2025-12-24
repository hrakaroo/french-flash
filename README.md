# French Flashcard Generator

A Python tool that generates Anki flashcards for learning French vocabulary. Provide your English-French vocabulary pairs, and it generates audio pronunciation files and creates ready-to-import Anki decks.

## 🤖 AI-Generated Project

This project was built entirely by directing Claude through the development process. **100% of the code is AI-generated.** This was a test project to see how AI can be used as a development partner to create functional, well-documented tools.

📖 For technical details and development context, see [CLAUDE.md](CLAUDE.md)

## Two Modes of Operation

This tool supports two distinct modes:

1. **📄 CSV Mode** - Work with local CSV files for offline vocabulary management
2. **☁️ Google Sheets Mode** - Edit vocabulary online and sync across devices

## How It Works

### Column Order

The script supports two column arrangements:

**English → French (Standard)**
```
English,French
hello,Bonjour
cat,chat
```
- **Card front**: English word
- **Card back**: French translation
- **Audio**: Pronounces the French word

**French → English (Reverse)**
```
French,English
Bonjour,hello
chat,cat
```
- **Card front**: French word
- **Card back**: English translation
- **Audio**: Pronounces the French word

The script automatically detects which column order you're using based on the header row. Audio always pronounces the French text, regardless of which side of the card it appears on.

### Formatting Options

You can enhance your flashcards with HTML formatting and special text handling:

**HTML Tags:**
- `<br>` - Line break (creates visual separation on cards)
- `<b>text</b>` - Bold text
- `<i>text</i>` - Italic text
- `<u>text</u>` - Underlined text

**Parentheses:**
- Text in parentheses `(like this)` appears on the card but is excluded from audio pronunciation
- Useful for grammar notes: `chat (m)` displays fully but pronounces only "chat"

**Audio Behavior:**
- HTML tags (except `<br>`) are removed from audio
- Text in parentheses is removed from audio
- `<br>` tags are converted to periods (`.`) in audio, creating natural pauses between lines

**Example:**
```csv
English,French
to be,"être<br><i>(irregular verb)</i>"
cat,"chat (m)"
```
- Cards display formatted text with line breaks and italics
- Audio pronounces only "être" and "chat" with natural pausing

## Features

- 🔊 Generates audio pronunciation files using Google Text-to-Speech
- 📇 Creates Anki flashcard decks (.apkg) ready to import
- ✏️ Requires French translations to be provided for all entries
- 🔀 Randomizes flashcard order each time you generate
- ⚡ Intelligent caching for Google Sheets - skips regenerating unchanged decks

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

---

## Mode 1: CSV Files (Local)

Use CSV mode when you want to work with local files on your computer. Perfect for offline use or when you prefer working with spreadsheet software like Excel or Numbers.

### Step 1: Create Your CSV File

Create a CSV file with two columns: `English` and `French`

**Standard Format (English → French):**
```csv
English,French
hello,Bonjour
goodbye,au revoir
cat,chat
dog,chien
thank you,merci
house,maison
```

**Reverse Format (French → English):**
You can also swap the columns to create cards where French is on the front:

```csv
French,English
Bonjour,hello
au revoir,goodbye
chat,cat
```

The script automatically detects swapped columns and creates cards accordingly.

Save this file (e.g., `deck/my_words.csv`)

### Step 2: Activate Virtual Environment

```bash
# Navigate to the project directory
cd /path/to/french-flash

# Activate the virtual environment
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3: Generate the Anki Deck

Run the script to create the flashcard deck:

```bash
python french_flashcards.py deck/my_words.csv
```

This will:
- Generate audio pronunciation files for all French words/phrases
- Create an Anki deck file at `output/my_words.apkg`
- Note: Text in parentheses `(like this)` and HTML tags `<br>` are kept on the card but excluded from audio

### Step 4: Import into Anki

1. Open Anki
2. Click "File" → "Import"
3. Select `output/my_words.apkg`
4. Click "Import"

Your French flashcards are now ready to study.

### Step 5: Deactivate Virtual Environment

When finished:

```bash
deactivate
```

---

## Mode 2: Google Sheets (Online)

Use Google Sheets mode when you want to edit vocabulary online, sync across devices, or collaborate with others. Requires one-time API setup.

### Prerequisites

Before using Google Sheets mode, you must complete the Google Sheets API setup:

📖 **[Complete Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)** - Follow this guide first to set up API access

### Step 1: Create Your Google Sheet

1. Create a new Google Sheet or open an existing one
2. Format it with two columns: `English` and `French` (or `French` and `English`)

**Example Google Sheet:**

| English | French |
|---------|--------|
| hello | Bonjour |
| goodbye | au revoir |
| cat | chat |
| dog | chien |

### Step 2: Share the Sheet with Your Service Account

After completing the API setup, you'll have a service account email (looks like `something@project-name.iam.gserviceaccount.com`).

1. Click the "Share" button in your Google Sheet
2. Paste the service account email
3. Give it "Viewer" or "Editor" access
4. Click "Send"

### Step 3: Get Your Spreadsheet ID

The Spreadsheet ID is in the URL of your Google Sheet:

```
https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz/edit
                                  ^^^^^^^^^^^^^^^^^^^^^^^^
                                  This is your Spreadsheet ID
```

Copy this ID - you'll need it to generate decks.

### Step 4: Activate Virtual Environment

```bash
# Navigate to the project directory
cd /path/to/french-flash

# Activate the virtual environment
source venv/bin/activate
```

### Step 5: Generate Anki Decks

**Option A: Generate from ALL sheets in the spreadsheet**
```bash
python french_flashcards.py -s YOUR_SPREADSHEET_ID
```

This will create a separate .apkg file for each sheet in your spreadsheet.

**Option B: Generate from ONE specific sheet**
```bash
python french_flashcards.py -s YOUR_SPREADSHEET_ID -n "Sheet Name"
```

Replace `"Sheet Name"` with the exact name of your sheet tab.

### Step 6: Import into Anki

1. Open Anki
2. Click "File" → "Import"
3. Select the generated `.apkg` file(s) from the `output/` directory
4. Click "Import"

### Step 7: Deactivate Virtual Environment

```bash
deactivate
```

### Google Sheets Features

**Rich Formatting:**
- **Multiline Text**: Press Alt+Enter (Cmd+Enter on Mac) to add line breaks → automatically converts to `<br>` tags
- **Bold Text**: Press Ctrl+B (Cmd+B on Mac) to make text bold → automatically wraps with `<b></b>` tags
- Format naturally in Google Sheets and the script handles the HTML conversion

**Intelligent Caching:**
- The script caches sheet content and skips regenerating unchanged decks
- Only sheets that have been modified will be regenerated
- Saves time and reduces API calls on repeated runs

**Multiple Sheets:**
- Organize different topics/lessons in separate sheets within one spreadsheet
- Generate all decks at once with `-s SPREADSHEET_ID`
- Or generate one specific deck with `-s SPREADSHEET_ID -n "Sheet Name"`

---

## Quick Reference

### CSV Mode
```bash
source venv/bin/activate                          # Activate environment
python french_flashcards.py deck/my_words.csv     # Generate deck
deactivate                                         # Deactivate when done
```

### Google Sheets Mode
```bash
source venv/bin/activate                          # Activate environment
python french_flashcards.py -s SPREADSHEET_ID     # All sheets
python french_flashcards.py -s SPREADSHEET_ID -n "Calendar"  # One sheet
deactivate                                         # Deactivate when done
```

### Get Help
```bash
python french_flashcards.py --help
```

---

## Output Files

The script generates:

- `output/<deck_name>.apkg` - Anki deck file (ready to import)
- `audio/*.mp3` - Audio pronunciation files (automatically included in .apkg)

**Note**: In Google Sheets mode, each sheet creates a separate .apkg file named after the sheet.

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
├── README.md                # This file - user documentation
├── CLAUDE.md                # Technical documentation
├── GOOGLE_SHEETS_SETUP.md   # Google Sheets API setup guide
├── deck/                    # CSV vocabulary files (optional)
├── audio/                   # Generated audio files (auto-created)
├── output/                  # Generated Anki decks (auto-created)
└── venv/                    # Virtual environment (auto-created)
```

## Requirements

- Python 3.13 or compatible version
- Internet connection (for TTS and Google Sheets API)


---

## Important Notes

### General
- ⚠️ Always activate the virtual environment before running the script
- 🌐 Requires an internet connection for text-to-speech
- ✏️ All French translations must be provided in your CSV or Google Sheet
- 🔊 Audio files are automatically embedded in the .apkg file
- 🔀 Flashcards are randomized each time you generate a deck

### CSV Mode Specific
- 📄 Works completely offline (except for audio generation)
- 💾 Store CSV files in the `deck/` directory for organization

### Google Sheets Mode Specific
- ☁️ Requires one-time API setup (see [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md))
- 🌐 Requires internet connection to fetch sheet data
- ⚡ Intelligent caching skips regenerating unchanged sheets
- 📊 Processes all sheets by default; use `-n` to target a specific sheet
- 🔄 Edit your sheet online and regenerate anytime

## License

MIT
