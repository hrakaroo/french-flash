# French Flashcard Generator

A Python tool that generates Anki flashcards for learning French vocabulary. Provide your English-French vocabulary pairs, and it generates audio pronunciation files and creates ready-to-import Anki decks.

## Features

- 🔊 Generates audio pronunciation files using Google Text-to-Speech
- 📇 Creates Anki flashcard decks (.apkg) ready to import
- ✏️ Requires French translations to be provided for all entries
- 🔀 Randomizes flashcard order each time you generate
- ☁️ Google Sheets support - edit vocabulary lists online from anywhere!
- ⚡ Intelligent caching - skips regenerating unchanged decks
- 🖼️ Optional automatic images - adds relevant images to English vocabulary cards using Pexels

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

Create a CSV file with two or three columns: `English`, `French`, and optionally `Image`

```csv
English,French,Image
hello,Bonjour,N
goodbye,au revoir,N
cat,chat,Y
dog,chien,Yes
thank you,merci,N
house,maison,Y
```

- **English column** (required): The English word or phrase
- **French column** (required): The French translation
- **Image column** (optional): Set to `Y` or `Yes` to fetch an image for this word

**Reverse Mode (French → English):**
You can also swap the columns to create cards where French is on the front:

```csv
French,English,Image
Bonjour,hello,N
au revoir,goodbye,N
chat,cat,N
```

The script automatically detects swapped columns and creates cards accordingly!

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

Your French flashcards are now ready to study!

### Step 5: Deactivate Virtual Environment

When finished:

```bash
deactivate
```

## Quick Reference

### CSV Files (Local)

```bash
# Activate virtual environment
source venv/bin/activate

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

**Formatting in Google Sheets:**
- **Multiline Text**: Press Alt+Enter (Cmd+Enter on Mac) to add line breaks → automatically converts to `<br>` tags
- **Bold Text**: Press Ctrl+B (Cmd+B on Mac) to make text bold → automatically wraps with `<b></b>` tags
- Just format naturally in Google Sheets and the script handles the HTML conversion!

**Caching**: The script automatically caches sheet content hashes. On subsequent runs, it will skip regenerating decks for sheets that haven't changed, saving time and API calls.

**📖 [Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)** - Complete instructions for setting up Google Sheets API access

## Output Files

The script generates:

- `output/<deck_name>.apkg` - Anki deck file (ready to import)
- `audio/*.mp3` - Audio pronunciation files (automatically included in .apkg)
- `images/*.jpg` - Downloaded images (when enabled, automatically included in .apkg)

## Configuration

Edit `config.py` to customize:

- `TTS_SLOW` - Set to `True` for slower pronunciation (useful for beginners)
- `ENABLE_IMAGES` - Set to `True` to enable automatic image fetching (requires Pexels API key)
- `PEXELS_API_KEY` - Your free Pexels API key (get one at https://www.pexels.com/api/)
- Directory paths
- Language settings

### Adding Images to Flashcards

To enable automatic image fetching for specific vocabulary words:

1. **Get a free Pexels API key**:
   - Visit https://www.pexels.com/api/
   - Click "Get Started" or "Sign Up"
   - Verify your email and log in
   - Go to your API page and copy your API key
   - **Rate limits**: Free tier allows 200 requests per hour, 20,000 per month

2. **Configure the script**:
   - Open `config.py`
   - Set `PEXELS_API_KEY = "your_api_key_here"`
   - Set `ENABLE_IMAGES = True`

3. **Add an Image column to your CSV or Google Sheet**:
   - Add a third column labeled `Image`
   - Set value to `Y` or `Yes` for words that should have images
   - Leave blank or set to `N` for words without images

   **CSV Example:**
   ```csv
   English,French,Image
   cat,chat,Y
   hello,bonjour,N
   house,maison,Yes
   ```

   **Google Sheets Example:**
   | English | French | Image |
   |---------|--------|-------|
   | cat     | chat   | Y     |
   | hello   | bonjour| N     |
   | house   | maison | Yes   |

4. **Generate flashcards as normal**:
   - Images will only be fetched for rows where Image = Y or Yes
   - Only applies when English is on the front of the card (not in reverse mode)
   - Images are cached locally to avoid re-downloading

**Note**: Images work best for concrete nouns (house, cat, car) and simple verbs (running, swimming). Abstract concepts may not get relevant images.

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
├── images/                  # Downloaded images (when ENABLE_IMAGES=True)
├── output/                  # Generated Anki decks (.apkg)
└── venv/                    # Virtual environment (created during setup)
```

## Requirements

- Python 3.13 or compatible version
- Internet connection (for TTS and Google Sheets API)

## HTML Formatting

You can use HTML in your French translations for better formatting:

```csv
English,French
hello,"Bonjour<br>Salut"
to be,"être<br><i>(irregular verb)</i>"
important word,"<b>Important</b>"
```

**Supported HTML tags:**
- `<br>` - Line break
- `<b>text</b>` - Bold text
- `<i>text</i>` - Italic text
- `<u>text</u>` - Underlined text

**Note:**
- HTML tags (except `<br>`) and text in parentheses are excluded from audio
- `<br>` tags are converted to periods (`.`) in audio to create natural pauses between lines
- The TTS will speak each line with a brief pause in between

## Notes

- ⚠️ Always activate the virtual environment before running the script
- 🌐 Requires an internet connection for text-to-speech and Google Sheets API
- 🔄 Supports both directions: `English,French` or `French,English` (detected automatically)
- 📝 Text in parentheses (e.g., "chat (m)") appears on cards but is excluded from audio
- 🎨 HTML tags (`<b>`, `<i>`, `<u>`) appear on cards but are excluded from audio
- ⏸️ Line breaks (`<br>`) create natural pauses in audio (converted to periods)
- ✏️ All French translations must be provided in your CSV or Google Sheet
- 🔊 Audio files are automatically embedded in the .apkg file
- ☁️ Google Sheets mode requires API setup (see [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md))
- 🔀 Flashcards are randomized each time you generate a deck
- ⚡ Intelligent caching skips regenerating unchanged Google Sheets decks
- 🖼️ Images are optional - only fetched when `ENABLE_IMAGES = True` AND the Image column is set to Y/Yes for that word

## License

MIT
