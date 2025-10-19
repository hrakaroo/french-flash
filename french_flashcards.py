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
from typing import List, Dict, Tuple
from deep_translator import GoogleTranslator
from gtts import gTTS
import genanki
import hashlib
import config


class FrenchFlashcardGenerator:
    """Generate French flashcards with audio pronunciation."""

    def __init__(self, deck_name: str = 'French Vocabulary'):
        self.translator = GoogleTranslator(source=config.SOURCE_LANG, target=config.TARGET_LANG)
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

    def translate_word(self, english: str, french: str = None) -> str:
        """
        Get French translation.
        If french is provided and not empty, return it.
        Otherwise, translate the English word/phrase.
        """
        # If French translation is provided, use it
        if french and french.strip():
            return french.strip()

        # Otherwise, translate it
        try:
            translation = self.translator.translate(english)
            return translation
        except Exception as e:
            print(f"Error translating '{english}': {e}")
            return english

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
        Process a list of English words/phrases with optional French translations.
        words: List of dicts with 'English' and 'French' keys
        Returns a dictionary with translation details.
        """
        results = {}

        for item in words:
            english = item['English']
            french_provided = item.get('French', '').strip()

            # Show whether translation was provided or will be looked up
            if french_provided:
                print(f"Processing: {english} (French provided)")
            else:
                print(f"Processing: {english} (looking up translation)")

            # Get French translation (use provided or translate)
            french = self.translate_word(english, french_provided)

            # Generate audio filename (use hash to avoid special characters)
            audio_filename = f"{hashlib.md5(english.encode()).hexdigest()}.mp3"

            # Generate audio
            generated_audio = self.generate_audio(french, audio_filename)

            # Create flashcard
            self.create_flashcard(english, french, generated_audio)

            results[english] = {
                'french': french,
                'audio': generated_audio,
                'was_provided': bool(french_provided)
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


def translate_csv(filename: str):
    """Translate missing French words in CSV and update the file."""
    print("Translation Mode")
    print("=" * 50)
    print(f"Processing file: {filename}\n")

    # Load existing CSV
    words = load_words_from_csv(filename)

    # Create translator
    translator = GoogleTranslator(source=config.SOURCE_LANG, target=config.TARGET_LANG)

    # Track changes
    translations_made = 0

    # Translate missing entries
    updated_words = []
    for item in words:
        english = item['English']
        french = item['French']

        if not french or not french.strip():
            # Translate it
            try:
                french = translator.translate(english)
                print(f"Translating: {english} → {french}")
                translations_made += 1
            except Exception as e:
                print(f"Error translating '{english}': {e}")
                french = ""
        else:
            print(f"Keeping: {english} → {french}")

        updated_words.append({
            'English': english,
            'French': french
        })

    # Write back to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['English', 'French']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_words)

    print("\n" + "=" * 50)
    print(f"Translations made: {translations_made}")
    print(f"CSV file updated: {filename}")
    print("\nRun without -t flag to generate flashcards.")


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
        '-t', '--translate',
        action='store_true',
        help='Translation mode: translate missing French words and update CSV (does not generate cards)'
    )

    args = parser.parse_args()
    csv_filename = args.csv_file

    # Check if file exists
    if not os.path.exists(csv_filename):
        print(f"Error: File '{csv_filename}' not found.")
        sys.exit(1)

    # Translation mode: just translate and update CSV
    if args.translate:
        translate_csv(csv_filename)
        return

    # Normal mode: generate flashcards
    # Load words from CSV file
    words = load_words_from_csv(csv_filename)

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
