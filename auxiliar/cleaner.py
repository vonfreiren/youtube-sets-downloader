import difflib
import re

import pandas as pd

from auxiliar.constants import remove_words


def define_separator(name):
    separators = ["live from", "live at", " - ", " @ ", " from ", " by ", " | ", " ｜ ", " | ", " | "]
    separator = " - "
    words = name.split()
    for word in words:
        for sep in separators:
            if sep.strip().upper() == word.strip().upper():
                separator = sep
                return separator

    return separator

def clean_song_title(song_title):

    song_title = re.sub(r'(?i)LIVE FROM', ' | ', song_title)
    song_title = re.sub(r'(?i)LIVE AT', ' | ', song_title)
    song_title = song_title.strip()

    return song_title


def clean_artist(artist, info):
    for word in remove_words:
        artist = artist.replace(word, "")
        artist = re.sub(r'\(.*?\)', '', artist)
        artist = get_similar_names(artist)
        artist = correct_artist(artist, info)
        if artist.isupper():
            artist = artist.title()
        artist = artist.strip()
    return artist

def correct_artist(artist, info):
    match = re.search(r'\b\d{4}\b', artist)
    if match:
        return info['uploader']
    return artist

def get_similar_names(artist):
    df = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')

    # Extract the features and labels

    y = df['Artist']
    y = list(y)

    similar_names = difflib.get_close_matches(artist.upper(), y, cutoff=0.7)
    if (len(similar_names) > 0):
        return similar_names[0]

    return artist

def clean_title(title):
    if title.isupper():
        title = title.title()
        return title


df = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')

# Extract the features and labels

y = df['Artist']
y = list(y)
artist = "arminvanbuuren"
similar_names = difflib.get_close_matches(artist.upper(), y, cutoff=0.7)
