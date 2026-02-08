# Polish Vocabulary Anki Deck

This project creates an Anki deck from a simple TSV file, automatically generating audio for each word using Google Text-to-Speech.

## Directory Structure

- `media/`: Contains the generated MP3 files.
- `vocabulary_anki_deck_polish_front.tsv`: The source file. Add new words here.
- `update_anki.py`: The script to generate audio and update the deck.
- `Polish_Vocabulary_Deck.apkg`: The importable Anki package.

## How to Add New Words

1.  **Edit the Source File:**
    Open `vocabulary_anki_deck_polish_front.tsv` and add your new words.
    Format:

    ```
    Polish Word    English Translation
    ```

    (Ensure there is a tab between the words)

2.  **Run the Script:**
    Open your terminal, navigate to this folder, and run:

    ```bash
    python3 update_anki.py
    ```

3.  **What the Script Does:**
    - Reads the new words.
    - Generates MP3 audio for the English translation (if it doesn't already exist).
    - Copies the audio files to your Anki `collection.media` folder.
    - Creates/Updates `Polish_Vocabulary_Deck.apkg`.

4.  **Update Anki:**
    - Double-click `Polish_Vocabulary_Deck.apkg`.
    - Anki will import the new cards and update any existing ones.

## Requirements

- Python 3
- `gTTS` library: `pip install gTTS`
- `genanki` library: `pip install genanki`
