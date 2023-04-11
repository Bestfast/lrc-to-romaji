import cutlet
import lrcparser
import os
import langid
import shutil
import logging

logger = logging.getLogger(__name__)

def transliterate(text):
    # Transliterate text from Japanese to Romaji using the Cutlet library
    return cutlet.Cutlet().romaji(text)

def backup_file(file_path):
    # Create a backup of a file if its contents are mostly in Japanese
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        lang, _ = langid.classify(text)
    if lang == "ja":
        backup_path = file_path + '.bak'
        logger.info(f"Backing up file {file_path} to {backup_path}")
        shutil.copy(file_path, backup_path)

def save_romaji_to_lrc(lyrics, translations, output_file):
    # Save transliterated lyrics to an LRC file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write LRC file header tags
        try:
            f.write('[ti:{}]'.format(lyrics.title))
            f.write('[ar:{}]'.format(lyrics.artist))
            f.write('[al:{}]'.format(lyrics.album))
            f.write('[by:{}]'.format(lyrics.editor))
            f.write('[offset:{}]'.format(lyrics.offset))
            f.write('[re:{}]'.format(lyrics.creator))
            f.write('\n')
        except:
            pass

        # Write transliterated lyrics with timestamps
        for timestamp, line in zip(lyrics.timestamps, translations):
            f.write('[{}]{}\n'.format(timestamp, line))
        logger.info("Saving the transliterated lyrics to LRC file")

def get_last_accessed_file(folder_path):
    # Get the path of the most recently accessed file in a folder
    files = os.listdir(folder_path)
    paths = [os.path.join(folder_path, basename) for basename in files]
    return max(paths, key=os.path.getatime)

def transliterate_last_accessed_file(folder_path):
    # Transliterate the lyrics of the most recently accessed LRC file in a folder
    file = get_last_accessed_file(folder_path)
    logger.info(f"Transliterating file: {file}")
    lyrics = lrcparser.LrcParser(file)

    # Translate each line and transliterate from Japanese to Romaji
    translations = []
    for line in lyrics.lyrics:
        romaji = transliterate(line)
        translations.append(romaji)
    
    # Create a backup of the original file and save the transliterated lyrics
    backup_file(file)
    save_romaji_to_lrc(lyrics, translations, file)