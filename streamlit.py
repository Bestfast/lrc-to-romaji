import streamlit as st
import lrcparser
import transliterate
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('streamlit.log', encoding='utf-8')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Read lyrics from file
file = transliterate.get_last_accessed_file(r"C:\Users\Bestfast\AppData\Roaming\foobar2000-v2\lyrics")
logger.info(f'Last accessed file: {file}')
lyrics = lrcparser.LrcParser(file)

# Translate each line and transliterate from Japanese to Romaji
translations = []
for line in lyrics.lyrics:
    if line.strip() != '':
        romaji = transliterate.transliterate(line)
    else:
        romaji = ''
    translations.append(romaji)

# Display transliterations on webpage
st.write('# Lyrics Translation')
# Textbox with all lyrics transliterated (scrollable and resizable)
all_translations = '\n'.join(translations)
st.text_area('All Translations', value=all_translations, height=400, max_chars=None)

for i, romaji in enumerate(translations):
    st.write(f'## Verse {i+1}')
    st.write(f'Japanese: {lyrics.lyrics[i]}')
    st.write(f'Romaji: {romaji}')
    
    # Allow user to select a verse to fix
    verse = lyrics.lyrics[i]
    words = verse.split()
    new_transliteration = []
    for j, word in enumerate(words):
        new_word = st.text_input(f'Transliterate "{word}":', value=transliterate.transliterate(word), key=f'{i}-{j}')
        new_transliteration.append(new_word)

    # Display updated Transliteration of selected verse
    updated_verse = ' '.join(new_transliteration)
    st.write(f'Word by word transliteration: {updated_verse}')

    st.write('---')

    # Save transliterated lyrics to LRC file
    if st.button('Save Verse {} to LRC'.format(i+1)):
        timestamp = lyrics.timestamps[i]
        translations[i] = updated_verse
        transliterate.backup_file(file)
        transliterate.save_romaji_to_lrc(lyrics, translations, file)
        st.write('Verse {} saved to LRC file'.format(i+1))
