import os
import re
from datetime import datetime

import eyed3
import yaml

from images.google_images import retrieve_image_cover, load_image

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path']
path_delete_mp4 = data['path_delete_mp4']
destination = path + "/"
list_values = []



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








