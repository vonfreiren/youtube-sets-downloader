import difflib
import re

import pandas as pd

from auxiliar.constants import remove_words


def define_separator(name):
    separators = ["live from", "live at", "Live @", "live @", "live",  " - ", " @ ", " from ", " by ", " | ", " ｜ ", " | ", " | "]
    separator = None
    words = name.split()
    for word in words:
        for sep in separators:
            if sep.strip().upper() == word.strip().upper():
                separator = word
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
    df_files_music = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')
    list_artists = df_files_music['Artist']
    list_artists = list(list_artists)
    similar_names = difflib.get_close_matches(artist.upper(), list_artists, cutoff=0.9)
    if len(similar_names)>0:
        return similar_names[0]
    match = re.search(r'\b\d{4}\b', artist)
    if match:
        return info['uploader']
    return artist

def get_similar_names(artist):
    df_music_files = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')
    artists = df_music_files['Artist']
    list_artists = list(artists)

    similar_names = difflib.get_close_matches(artist.upper(), list_artists, cutoff=0.7)
    if len(similar_names) > 0:
        return similar_names[0]

    return artist

def get_exact_name(artist):
    df_music_files = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')
    artists_list = df_music_files['Artist']
    artists_list = list(artists_list)
    artists_list = [x.upper() for x in artists_list]

    if artist.upper() in artists_list:
        return True

    return False
