import os
import re
from datetime import datetime

import eyed3
import yaml
from pytube import YouTube
from termcolor import colored
from yt_dlp import YoutubeDL

from auxiliar.cleaner import clean_song_title, define_separator, clean_artist
from images.google_images import retrieve_image_cover, load_image

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path']
path_delete_mp4 = data['path_delete_mp4']
destination = path + "/"
list_values = []

def convert(url):
    ydl_opts = {
        'outtmpl': destination + '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

        info = ydl.extract_info(url, download=False)
        name = ydl.prepare_filename(info)
        name = name.replace(".webm", ".mp3")
        name = name.replace(".m4a", ".mp3")
        name = name.replace('"', '')
        song_title = YouTube(url).title

        song_title = clean_song_title(song_title)
        separator = define_separator(song_title)

        artist = song_title.split(separator)[0]
        split_index = song_title.find(separator) + 1
        title = song_title[split_index+1:]
        title = title.strip()
        artist = clean_artist(artist, info)
        year = get_year(song_title, info)

        create_tag(name, year, artist, title, song_title)
        list_values.append([name, artist, title, year])

        success_message = "Downloaded: " + name
        print(colored(success_message, 'green'))


def create_tag(name, year, artist, title, song_title):
    audio = eyed3.load(name)
    audio.initTag()

    audio.tag.release_date = year
    audio.tag.recording_date = year
    audio.tag.tagging_date = year
    audio.tag.release_date = year
    audio.tag.org_recording_date = year

    audio.tag.artist = artist
    audio.tag.album = title
    audio.tag.title = title
    audio.tag.album_artist = artist

    audio.tag.genre = "Electronic"

    cover_image = retrieve_image_cover(song_title)
    audio = load_image(audio, cover_image)

    audio.tag.save(version=eyed3.id3.ID3_V2_3)







def get_year(name, info):
    match = re.search(r'\d{4}', name)
    if match:
        return match.group()
    else:
        if 'release_date' in info:
            try:
                year = info['release_date'][0:4]
                return year
            except:
                return datetime.now().year




