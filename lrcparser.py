import re


class LrcParser:
    def __init__(self, file):
        self.file = file
        self.lyrics = []
        self.timestamps = []
        self.timestamped_lyrics = []
        self.parse()

    def parse(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            match = re.findall(r'\[(\d+:\d+\.\d+)\]', line)
            if match:
                for timestamp in match:
                    lyrics = re.sub(r'\[(\d+:\d+\.\d+)\]', '', line).strip()
                    self.timestamps.append(timestamp)
                    self.lyrics.append(lyrics)
                    self.timestamped_lyrics.append((timestamp, lyrics))

    def get_lyrics(self):
        lyrics_without_timestamps = []
        for lyric in self.lyrics:
            # Remove any timestamps from the lyric
            lyric_without_timestamps = re.sub(
                r'\[\d+:\d+\.\d+\]', '', lyric).strip()
            if lyric_without_timestamps:
                lyrics_without_timestamps.append(lyric_without_timestamps)
        return '\n'.join(lyrics_without_timestamps)

    def get_timestamped_lyrics(self):
        lines = []
        for timestamp, lyric in self.timestamped_lyrics:
            line = f'[{timestamp}] {lyric}'
            lines.append(line)

        return '\n'.join(lines)

    def get_timestamps(self):
        return self.timestamps
