import genanki
import csv
import os
import re
import shutil
from gtts import gTTS

# --- CONFIGURATION ---
INPUT_TSV = 'vocabulary_anki_deck_polish_front.tsv'
OUTPUT_TSV = 'vocabulary_anki_deck_polish_front_with_audio.tsv' # Can be same as input to overwrite
OUTPUT_APKG = 'Polish_Vocabulary_Deck.apkg'
MEDIA_DIR = 'media'
ANKI_MEDIA_DIR = '/Users/barty/Library/Application Support/Anki2/User 1/collection.media/'

# IMPORTANT: Fix these IDs to update the SAME deck each time
MODEL_ID = 1678901234
DECK_ID = 2023050101

# --- SETUP ---
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# --- AUDIO GENERATION ---
print(f"Reading {INPUT_TSV}...")
rows = []
try:
    with open(INPUT_TSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        rows = list(reader)
except FileNotFoundError:
    print(f"Error: {INPUT_TSV} not found. Please create it first.")
    exit()

# Handle header
header = rows[0] if rows else []
data_rows = rows[1:] if rows and header and header[0] == 'Front' else rows

print(f"Checking audio for {len(data_rows)} words...")

processed_rows = []
media_files = []

for row in data_rows:
    if len(row) < 2:
        continue
    
    front = row[0].strip()
    back = row[1].strip()
    
    # Generate clean filename from English back
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', back.lower())
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    audio_filename = f"{clean_name}.mp3"
    audio_path = os.path.join(MEDIA_DIR, audio_filename)
    
    # Generate MP3 if missing
    if not os.path.exists(audio_path):
        try:
            print(f"Generating audio for: {back}")
            tts = gTTS(text=back, lang='en')
            tts.save(audio_path)
        except Exception as e:
            print(f"Failed to generate audio for '{back}': {e}")
    
    # Add to media list for package
    if os.path.exists(audio_path):
        media_files.append(audio_path)
        # Copy to Anki folder directly
        try:
            shutil.copy2(audio_path, ANKI_MEDIA_DIR)
        except Exception as e:
            print(f"Failed to copy to Anki folder: {e}")

    # Create note fields
    audio_field = f"[sound:{audio_filename}]"
    processed_rows.append([front, back, audio_field])

# --- ANKI PACKAGE CREATION ---
print("Creating Anki package...")

my_model = genanki.Model(
  MODEL_ID,
  'Basic Polish Vocabulary (Audio)',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
    {'name': 'Audio'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{Audio}}',
    },
  ])

my_deck = genanki.Deck(
  DECK_ID,
  'Polish Vocabulary with Audio')

for row in processed_rows:
    note = genanki.Note(
        model=my_model,
        fields=row)
    my_deck.add_note(note)

my_package = genanki.Package(my_deck)
my_package.media_files = media_files
my_package.write_to_file(OUTPUT_APKG)

print(f"\nSUCCESS! Created {OUTPUT_APKG} with {len(my_deck.notes)} notes.")
print(f"Audio files copied to: {ANKI_MEDIA_DIR}")
print("\nTo update Anki:")
print(f"1. Simply double-click '{OUTPUT_APKG}'")
print("2. Anki will update existing cards and add new ones.")
