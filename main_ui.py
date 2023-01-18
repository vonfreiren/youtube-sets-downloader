import re
import sys
from datetime import datetime

import eyed3
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, \
    QSpacerItem, QMessageBox
from pytube import YouTube
import os
import yaml
from yt_dlp import YoutubeDL

from auxiliar.cleaner import clean_song_title, define_separator, clean_artist, correct_artist
from images.google_images import retrieve_image_cover, load_image

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path']
path_delete_mp4 = data['path_delete_mp4']
destination = path + "/"


def convert(list_urls, quality=192):
    ydl_opts = {
        'outtmpl': destination + '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
            'quiet': True,
            'logger': YoutubeDL.utils.null_logger
        }],
    }
    print(list_urls)

    for url in list_urls:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

            info = ydl.extract_info(url, download=False)
            name = ydl.prepare_filename(info)
            name = name.replace(".webm", ".mp3")
            name = name.replace(".m4a", ".mp3")
            song_title = YouTube(url).title
            print(name)

            song_title = clean_song_title(song_title)
            separator = define_separator(song_title)

            artist = song_title.split(separator)[0]
            split_index = song_title.find(separator) + 1
            title = song_title[split_index+1:]
            title = title.strip()
            artist = clean_artist(artist, info)
            year = get_year(song_title, info)

            create_tag(name, year, artist, title, song_title)


            print("downloaded: " + name)
            list_urls.remove(url)

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
            except:
                return datetime.now().year




class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.list_values = []
        self.setWindowTitle('Youtube Videos to  mp3')
        self.setGeometry(400, 400, 400, 300)

        self.input_field = QLineEdit()
        layout.addSpacerItem(QSpacerItem(200, 0))

        self.input_field.setPlaceholderText("Enter a valid Youtube URL")
        layout.addSpacerItem(QSpacerItem(200, 0))

        self.add_button = QPushButton("Add URL")
        self.add_button.clicked.connect(self.add_value)

        layout.addSpacerItem(QSpacerItem(200, 0))

        self.download_button = QPushButton("Download mp3")
        self.download_button.clicked.connect(self.download)

        self.values_label = QLabel("URLs:")

        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.add_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.values_label)
        self.setLayout(layout)

    def add_value(self):
        value = self.input_field.text()
        if value:
            try:
                self.list_values.append(value)
                text = "Videos to be downloaded: "
                for value in self.list_values:
                    video = YouTube(value)
                    text += "\n" + video.title
                self.values_label.setText(text)
                self.input_field.clear()
            except:
                self.values_label.setText("Invalid URL")

    def download(self):
        if len(self.list_values) > 0:
            print(len(self.list_values))
            convert(self.list_values)
        else:
            self.values_label.setText("No URLs to download")




if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
