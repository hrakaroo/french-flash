#!/usr/bin/env python3
"""
French Flashcard Generator
Translates English words to French, generates audio pronunciation,
and creates Anki flashcards.
"""

import os
import sys
import csv
import argparse
import re
import random
import json
from typing import List, Dict, Tuple, Optional
from gtts import gTTS
import genanki
import hashlib
import gspread
from google.oauth2.service_account import Credentials
import config


class FrenchFlashcardGenerator:
    """Generate French flashcards with audio pronunciation."""

    def __init__(self, deck_name: str = 'French Vocabulary'):
        self.audio_files = []
        self.deck_name = deck_name

        # Create Anki model for flashcards
        self.model = genanki.Model(
            1607392319,
            'French Vocabulary',
            fields=[
                {'name': 'English'},
                {'name': 'French'},
                {'name': 'Audio'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{English}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{French}}<br>{{Audio}}',
                },
            ])

        # Generate unique deck ID from deck name
        deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16)

        # Create deck with custom name and unique ID
        self.deck = genanki.Deck(
            deck_id,
            deck_name)

    def get_french_translation(self, english: str, french: str = None) -> str:
        """
        Get French translation from provided value.
        French translation must be provided - no automatic lookup.
        """
        if french and french.strip():
            return french.strip()

        # No French translation provided - this is an error
        print(f"Error: Missing French translation for '{english}'")
        return ""

    def generate_audio(self, text: str, filename: str) -> str:
        """Generate audio file for French text using Google TTS."""
        try:
            # Remove anything in parentheses before generating audio
            clean_text = re.sub(r'\([^)]*\)', '', text).strip()

            filepath = os.path.join(config.AUDIO_DIR, filename)
            tts = gTTS(text=clean_text, lang=config.TTS_LANGUAGE, slow=config.TTS_SLOW)
            tts.save(filepath)
            self.audio_files.append(filepath)
            return filename
        except Exception as e:
            print(f"Error generating audio for '{text}': {e}")
            return ""

    def create_flashcard(self, english: str, french: str, audio_filename: str):
        """Create an Anki flashcard."""
        # Format audio
        audio_tag = f"[sound:{audio_filename}]" if audio_filename else ""

        note = genanki.Note(
            model=self.model,
            fields=[english, french, audio_tag]
        )
        self.deck.add_note(note)

    def process_words(self, words: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        """
        Process a list of English words/phrases with French translations.
        words: List of dicts with 'English' and 'French' keys
        Returns a dictionary with processing details.
        """
        results = {}

        for item in words:
            english = item['English']
            french_provided = item.get('French', '').strip()

            # Get French translation (must be provided)
            french = self.get_french_translation(english, french_provided)

            # Skip if no French translation
            if not french:
                print(f"Skipping: {english} (no French translation provided)")
                continue

            print(f"Processing: {english}")

            # Generate audio filename (use hash to avoid special characters)
            audio_filename = f"{hashlib.md5(english.encode()).hexdigest()}.mp3"

            # Generate audio
            generated_audio = self.generate_audio(french, audio_filename)

            # Create flashcard
            self.create_flashcard(english, french, generated_audio)

            results[english] = {
                'french': french,
                'audio': generated_audio
            }

            print(f"  → {french}")

        return results

    def save_deck(self, filename: str = None):
        """Save the Anki deck to a file."""
        if filename is None:
            filename = f"{self.deck_name.lower().replace(' ', '_')}.apkg"

        output_path = os.path.join(config.OUTPUT_DIR, filename)

        # Create package with audio files
        package = genanki.Package(self.deck)
        package.media_files = self.audio_files
        package.write_to_file(output_path)

        print(f"\nAnki deck saved to: {output_path}")
        return output_path



def load_words_from_csv(filename: str = 'example_words.csv') -> List[Dict[str, str]]:
    """Load words from CSV file with English and French columns."""
    words = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append({
                'English': row['English'],
                'French': row.get('French', '').strip()
            })
    return words


def get_google_sheets_client():
    """Create and return authenticated Google Sheets client."""
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]

        creds = Credentials.from_service_account_file(
            config.GOOGLE_CREDENTIALS_FILE,
            scopes=scopes
        )

        return gspread.authorize(creds)

    except FileNotFoundError:
        print(f"Error: Credentials file '{config.GOOGLE_CREDENTIALS_FILE}' not found.")
        print("Please follow the setup instructions in GOOGLE_SHEETS_SETUP.md")
        sys.exit(1)
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        sys.exit(1)


def get_all_sheet_names(spreadsheet_id: str) -> List[str]:
    """Get list of all sheet names in a spreadsheet."""
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(spreadsheet_id)
        return [worksheet.title for worksheet in spreadsheet.worksheets()]
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{spreadsheet_id}' not found.")
        print("Check that the spreadsheet ID is correct and shared with your service account.")
        sys.exit(1)
    except Exception as e:
        print(f"Error getting sheet names: {e}")
        sys.exit(1)


def load_words_from_sheet(spreadsheet_id: str, sheet_name: str) -> List[Dict[str, str]]:
    """Load words from Google Sheet with English and French columns."""
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        # Get all records as list of dictionaries
        records = worksheet.get_all_records()

        # Convert to our expected format
        words = []
        for row in records:
            words.append({
                'English': str(row.get('English', '')),
                'French': str(row.get('French', '')).strip()
            })

        return words

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{spreadsheet_id}' not found.")
        print("Check that the spreadsheet ID is correct and shared with your service account.")
        sys.exit(1)
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Sheet '{sheet_name}' not found in spreadsheet.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading Google Sheet: {e}")
        sys.exit(1)


def compute_sheet_hash(words: List[Dict[str, str]]) -> str:
    """Compute hash of sheet content for caching."""
    # Create a deterministic string representation of the data
    content = json.dumps(words, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def load_cache() -> Dict[str, Dict[str, str]]:
    """Load cache from disk."""
    if os.path.exists(config.SHEET_CACHE_FILE):
        try:
            with open(config.SHEET_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache file: {e}")
            return {}
    return {}


def save_cache(cache: Dict[str, Dict[str, str]]):
    """Save cache to disk."""
    try:
        with open(config.SHEET_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Could not save cache file: {e}")


def is_sheet_cached(spreadsheet_id: str, sheet_name: str, current_hash: str) -> bool:
    """Check if sheet content matches cached hash."""
    cache = load_cache()
    cache_key = f"{spreadsheet_id}:{sheet_name}"

    if cache_key in cache:
        cached_entry = cache[cache_key]
        return cached_entry.get('hash') == current_hash

    return False


def update_cache(spreadsheet_id: str, sheet_name: str, content_hash: str, output_file: str):
    """Update cache with new sheet hash and output file."""
    cache = load_cache()
    cache_key = f"{spreadsheet_id}:{sheet_name}"

    cache[cache_key] = {
        'hash': content_hash,
        'output_file': output_file,
        'last_generated': os.path.getmtime(os.path.join(config.OUTPUT_DIR, output_file)) if os.path.exists(os.path.join(config.OUTPUT_DIR, output_file)) else None
    }

    save_cache(cache)


def get_deck_name_from_filename(filename: str) -> str:
    """Convert filename to deck name (e.g., 'example_words.csv' -> 'Example Words')."""
    # Get just the basename without path
    basename = os.path.basename(filename)
    # Remove .csv extension
    name = basename.replace('.csv', '')
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    # Capitalize each word
    return name.title()


def main():
    """Main function to run the flashcard generator."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='French Flashcard Generator - Translate words and create Anki decks'
    )
    parser.add_argument(
        'csv_file',
        nargs='?',
        default='basic_french.csv',
        help='CSV file with English/French words (default: basic_french.csv)'
    )
    parser.add_argument(
        '-s', '--sheet',
        metavar='SPREADSHEET_ID',
        help='Use Google Sheets instead of CSV. Provide spreadsheet ID.'
    )
    parser.add_argument(
        '-n', '--sheet-name',
        metavar='SHEET_NAME',
        default=None,
        help='Name of specific sheet to use in Google Spreadsheet (default: process all sheets)'
    )

    args = parser.parse_args()

    # Determine input source: Google Sheets or CSV
    using_sheets = args.sheet is not None

    if using_sheets:
        # Google Sheets mode
        spreadsheet_id = args.sheet
        sheet_name = args.sheet_name

        print("French Flashcard Generator (Google Sheets)")
        print("=" * 50)
        print(f"Spreadsheet ID: {spreadsheet_id}")

        # Determine which sheets to process
        if sheet_name:
            # Process single sheet
            sheet_names = [sheet_name]
            print(f"Sheet: {sheet_name}")
        else:
            # Process all sheets
            print("Getting all sheets from spreadsheet...")
            sheet_names = get_all_sheet_names(spreadsheet_id)
            print(f"Found {len(sheet_names)} sheets: {', '.join(sheet_names)}")

        print("\n" + "=" * 50)

        # Process each sheet
        for idx, current_sheet_name in enumerate(sheet_names, 1):
            if len(sheet_names) > 1:
                print(f"\n[{idx}/{len(sheet_names)}] Processing sheet: {current_sheet_name}")
                print("-" * 50)

            # Load words from Google Sheets
            words = load_words_from_sheet(spreadsheet_id, current_sheet_name)

            if not words:
                print(f"Skipping empty sheet: {current_sheet_name}\n")
                continue

            # Get output filename from sheet name (preserve case, replace spaces with underscores)
            output_filename = f"{current_sheet_name.replace(' ', '_')}.apkg"
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)

            # Compute hash of sheet content
            content_hash = compute_sheet_hash(words)

            # Check if sheet is already cached and output file exists
            if is_sheet_cached(spreadsheet_id, current_sheet_name, content_hash) and os.path.exists(output_path):
                print(f"✓ Skipping '{current_sheet_name}' - no changes detected (using cached {output_filename})")
                continue

            # Sheet has changed or doesn't exist, generate deck
            # Randomize the order of words
            random.shuffle(words)

            # Create deck name from sheet name
            deck_name = current_sheet_name.replace('_', ' ').title()

            print(f"Deck: {deck_name}")
            print(f"Processing {len(words)} words...\n")

            generator = FrenchFlashcardGenerator(deck_name=deck_name)
            results = generator.process_words(words)

            # Save outputs
            print("\n" + "-" * 50)
            generator.save_deck(output_filename)

            # Update cache with new hash
            update_cache(spreadsheet_id, current_sheet_name, content_hash, output_filename)

        print("\n" + "=" * 50)
        print("\nDone! Import the .apkg file(s) into Anki to use your flashcards.")
        return

    else:
        # CSV mode
        csv_filename = args.csv_file

        # Check if file exists
        if not os.path.exists(csv_filename):
            print(f"Error: File '{csv_filename}' not found.")
            sys.exit(1)

        # Load words from CSV file
        words = load_words_from_csv(csv_filename)

        # Randomize the order of words
        random.shuffle(words)

        # Create deck name from filename
        deck_name = get_deck_name_from_filename(csv_filename)

        # Get output filename from input basename
        basename = os.path.basename(csv_filename)
        output_filename = basename.replace('.csv', '.apkg')

        print("French Flashcard Generator")
        print("=" * 50)
        print(f"Input file: {csv_filename}")
        print(f"Deck: {deck_name}")
        print(f"Processing {len(words)} words...\n")

        generator = FrenchFlashcardGenerator(deck_name=deck_name)
        results = generator.process_words(words)

        # Save outputs
        print("\n" + "=" * 50)
        generator.save_deck(output_filename)

        print("\nDone! Import the .apkg file into Anki to use your flashcards.")


if __name__ == "__main__":
    main()
