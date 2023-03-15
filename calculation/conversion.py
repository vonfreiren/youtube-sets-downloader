import os
import re
from datetime import datetime

import yaml
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TYER
from mutagen.mp3 import MP3
from pytube import YouTube
from termcolor import colored
from yt_dlp import YoutubeDL

from auxiliar.cleaner import clean_song_title, define_separator, clean_artist, get_exact_name
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
            'preferredquality': '192',
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
        festival_name = False

        if separator is None:
            separator = find_festival_name(song_title)
            if separator is not None:
                festival_name = True

        split_song_title = song_title.split(separator)
        artist = split_song_title[0]
        if festival_name:
            title = separator + " " + split_song_title[1]
        else:
            if separator is None:
                separator = " "
            title = split_song_title[1]
            if len(split_song_title) > 2:
                for i in range(2, len(split_song_title)):
                    title = title + separator + split_song_title[i]
        title = title.strip()

        if is_inverse(title):
            temp_artist = artist
            artist = title
            title = temp_artist

        artist = clean_artist(artist, info)

        year = get_year(song_title, info)

        create_tag(name, year, artist, title, song_title)
        list_values.append([name, artist, title, year])

        success_message = "Downloaded: " + name
        print(colored(success_message, 'green'))

def is_inverse(name):
    if get_exact_name(name):
        return True
    return False
def find_festival_name(name):
    festivals = ["Tomorrowland", "Ultra Music Festival", "EDC", "Creamfields", "Tomorrowland Winter", "Tomorrowland Brasil"]
    for festival in festivals:
        if festival in name:
            return festival

    return None


def create_tag(name, year, artist, title, song_title):


    audio = MP3(name, ID3=ID3)
    audio.ID3.version = (3, 2)

    # add title tag
    audio.tags.add(TIT2(encoding=3, text=title))

    # add artist tag
    audio.tags.add(TPE1(encoding=3, text=artist))

    # add album tag
    audio.tags.add(TALB(encoding=3, text=artist))

    audio.tags.add(TALB(encoding=3, text=title))

    audio.tags.add(TYER(encoding=3, text=year))

    # add genre tag
    audio.tags.add(TCON(encoding=3, text="Electronic"))

    audio.save()



    try:
        cover_image = retrieve_image_cover(song_title)
        audio = load_image(audio, cover_image, name)
    except:
        print("error with image")

    audio.save()








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

        elif 'upload_date' in info:
            try:
                year = info['upload_date'][0:4]
                return year
            except:
                return datetime.now().year

    return datetime.now().year





