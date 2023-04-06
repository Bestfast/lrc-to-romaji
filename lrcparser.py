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
            if re.match(r'\[\d+:\d+\.\d+\]', line):
                timestamp = line.split(']')[0][1:]
                self.timestamps.append(timestamp)
                lyrics = line.split(']')[-1].strip()
                self.lyrics.append(lyrics)
                self.timestamped_lyrics.append((timestamp, lyrics))

    def get_lyrics(self):
        return '\n'.join(self.lyrics)

    def get_timestamped_lyrics(self):
        return '\n'.join([f'[{t}] {l}' for t, l in self.timestamped_lyrics])

    def get_timestamps(self):
        return self.timestamps
