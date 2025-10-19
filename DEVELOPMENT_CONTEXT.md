# Development Context - French Flashcard Generator

## Current State (2025-10-08)

### What We Just Completed
1. ✅ Created Python project for French flashcard generation with Anki integration
2. ✅ Set up virtual environment with Python 3.13 compatibility
3. ✅ Implemented translation using deep-translator (Google Translate API)
4. ✅ Added audio generation using Google Text-to-Speech (gTTS)
5. ✅ Created Anki deck generation with genanki
6. ✅ Implemented CSV-based word type specification (n=noun, v=verb)
7. ✅ Added indefinite article detection for French nouns (un/une)
8. ✅ Made deck names and output filenames derive from input CSV filename
9. ✅ Added command-line argument support for input file
10. ✅ Fixed duplicate deck issue with unique deck ID generation
11. ✅ Created two CSV files: `example_words.csv` and `basic_fifty.csv`

### Current Files
- `french_flashcards.py` - Main application (fully functional)
- `config.py` - Configuration settings
- `requirements.txt` - deep-translator, gTTS, genanki
- `README.md` - Complete documentation with virtual env instructions
- `example_words.csv` - Sample words (20 entries)
- `basic_fifty.csv` - 50 common words (6 phrases, 27 nouns, 17 verbs)
- `.gitignore` - Ignores venv/, audio/, output/, etc.

### Last Issue Resolved
**Problem**: Anki only showed 20 cards when importing "Basic Fifty" deck (50 words expected)
**Root Cause**: Hardcoded deck ID caused Anki to treat all decks as the same deck
**Solution**: Generate unique deck ID using MD5 hash of deck name (line 45 in french_flashcards.py)

### How to Resume After Reboot

1. **Activate virtual environment:**
   ```bash
   cd /Users/jgerth/GitHub/french-flash
   source venv/bin/activate
   ```

2. **Test the fix:**
   ```bash
   python french_flashcards.py basic_fifty.csv
   ```

3. **Import into Anki:**
   - Import `output/basic_fifty.apkg`
   - Should now see all 50 cards

### Known Working State
- Virtual environment created and dependencies installed
- Script runs successfully with both CSV files
- Generates .apkg files with audio
- Articles correctly added only to nouns
- Each deck has unique ID based on name

### Potential Next Steps (Not Started)
- Add batch processing for multiple CSV files
- Add progress bar for long word lists
- Add error handling for network failures
- Add caching for translations to avoid re-translating
- Support for adjectives or other word types
- Add reverse cards (French → English)
- Support for example sentences

### Environment
- OS: macOS (Darwin 24.6.0)
- Python: 3.13
- Working Directory: `/Users/jgerth/GitHub/french-flash`
- Git repo: Not initialized

### Dependencies Installed
```
deep-translator==1.11.4
gTTS==2.5.3
genanki==0.13.1
```

### Commands Reference
```bash
# Activate venv
source venv/bin/activate

# Run with specific file
python french_flashcards.py basic_fifty.csv

# Run with default
python french_flashcards.py

# Deactivate venv
deactivate

# Install dependencies (if needed)
pip install -r requirements.txt
```

### CSV Format Template
```csv
word,type
<english_word>,n    # noun - will get un/une
<english_word>,v    # verb - no article
<english_word>,     # other - no article
```

## Notes
- No git repository initialized (user said "Is directory a git repo: No")
- All audio files stored in `audio/` directory (git-ignored)
- All output files stored in `output/` directory
- Requires internet connection for translation and TTS
