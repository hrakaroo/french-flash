# Google Sheets Setup Guide

This guide walks you through setting up Google Sheets API access for the French Flashcard Generator.

## Overview

Using Google Sheets allows you to:
- Edit your vocabulary lists from anywhere
- Collaborate with others on vocabulary
- Keep multiple decks in one spreadsheet (different sheets)
- No need to sync CSV files manually

## Setup Steps

### 1. Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Enable the **Google Drive API** (also required):
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - **Service account name**: `french-flashcards` (or any name you prefer)
   - **Service account ID**: Will be auto-filled
   - Click "Create and Continue"
4. Skip the optional steps (click "Done")
5. Click on the newly created service account
6. Go to the "Keys" tab
7. Click "Add Key" > "Create new key"
8. Choose **JSON** format
9. Click "Create" - a JSON file will download

### 3. Install the Credentials File

1. Rename the downloaded JSON file to `credentials.json`
2. Move it to your `french-flash` project directory
3. **Important**: This file contains sensitive credentials - never share it or commit it to git!

### 4. Share Your Spreadsheet

1. Open (or create) your Google Spreadsheet
2. Click the "Share" button
3. Copy the **service account email** from your credentials file
   - It looks like: `french-flashcards@PROJECT_ID.iam.gserviceaccount.com`
   - You can find it in `credentials.json` under `"client_email"`
4. Paste the service account email in the "Add people and groups" field
5. Set permission to **Viewer** (read-only is sufficient)
6. Click "Send"

### 5. Get Your Spreadsheet ID

The spreadsheet ID is in the URL of your Google Sheet:

```
https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit
                                      ^^^^^^^^^^^^^^^^^^^^
                                      This is your Spreadsheet ID
```

Copy this ID - you'll need it to generate flashcards.

### 6. Format Your Spreadsheet

Your Google Sheet should have two columns with headers:

| English | French |
|---------|--------|
| hello   | Bonjour |
| goodbye | au revoir |
| cat     | chat |

- **First row must be headers**: `English` and `French`
- **English column** (required): The English word or phrase
- **French column** (optional): Leave empty for auto-translation, or provide your own
- Each sheet in your spreadsheet can be a different deck

### 7. Install Dependencies

Update your Python packages:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Generate Flashcards from Google Sheets

```bash
# Basic usage - processes ALL sheets in the spreadsheet
python french_flashcards.py -s YOUR_SPREADSHEET_ID

# Process only a specific sheet
python french_flashcards.py -s YOUR_SPREADSHEET_ID -n "Basic Vocabulary"

# Example with real spreadsheet ID (all sheets)
python french_flashcards.py -s 1A2B3C4D5E6F7G8H9I0J

# Example with specific sheet
python french_flashcards.py -s 1A2B3C4D5E6F7G8H9I0J -n "Calendar"
```

### Examples

```bash
# Generate decks from ALL sheets in the spreadsheet
python french_flashcards.py -s 1A2B3C4D5E6F7G8H9I0J

# Generate from only the "Verbs" sheet
python french_flashcards.py -s 1A2B3C4D5E6F7G8H9I0J -n Verbs

# Generate from only the "Common Phrases" sheet
python french_flashcards.py -s 1A2B3C4D5E6F7G8H9I0J -n "Common Phrases"
```

**Default Behavior**: When you don't specify a sheet name with `-n`, the script will automatically process **all sheets** in your spreadsheet and generate a separate `.apkg` deck file for each one!

## Spreadsheet Organization Tips

You can organize multiple decks in one spreadsheet using different sheets:

**One Spreadsheet with Multiple Sheets:**
- Sheet: "Basic Words"
- Sheet: "Verbs"
- Sheet: "Calendar"
- Sheet: "House"

Simply run: `python french_flashcards.py -s YOUR_SPREADSHEET_ID`

This will automatically generate 4 separate deck files:
- `Basic_Words.apkg`
- `Verbs.apkg`
- `Calendar.apkg`
- `House.apkg`

**Note**: Output filenames preserve the case from your sheet names, with spaces replaced by underscores.

**Want just one sheet?** Use the `-n` flag:
- `python french_flashcards.py -s ID -n Verbs` → generates only `Verbs.apkg`

## Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the project root directory
- Check that the filename is exactly `credentials.json`

### "Spreadsheet not found"
- Verify the spreadsheet ID is correct
- Make sure you shared the spreadsheet with your service account email
- Check that the service account has at least Viewer permission

### "Sheet not found"
- Check the sheet name spelling (case-sensitive!)
- Make sure the sheet exists in your spreadsheet

### "Permission denied"
- Ensure Google Sheets API and Google Drive API are both enabled
- Verify you shared the spreadsheet with the service account

## Security Notes

- **Never commit `credentials.json` to git** (it's already in `.gitignore`)
- Keep your service account credentials secure
- Only share spreadsheets with the service account email (not your personal email)
- If credentials are compromised, delete the service account and create a new one

## CSV vs Google Sheets

| Feature | CSV | Google Sheets |
|---------|-----|---------------|
| Edit anywhere | ❌ No | ✅ Yes |
| Requires internet | ❌ No | ✅ Yes |
| Setup complexity | ✅ Simple | ⚠️ Moderate |
| Translation mode | ✅ Yes | ❌ No* |
| Collaboration | ❌ No | ✅ Yes |

*For Google Sheets, translate directly in the sheet or export to CSV for translation mode.

## Still Using CSV?

CSV files still work great! You can use both methods:

```bash
# Use CSV
python french_flashcards.py deck/basic_fifty.csv

# Use Google Sheets
python french_flashcards.py -s YOUR_SPREADSHEET_ID
```
