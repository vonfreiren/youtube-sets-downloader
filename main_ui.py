import os
import sys

import yaml
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, \
    QSpacerItem
from pytube import YouTube

from calculation.conversion import convert

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path']
path_delete_mp4 = data['path_delete_mp4']
destination = path + "/"














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
            for url in self.list_values:
                convert(url)
        else:
            self.values_label.setText("No URLs to download")




if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
