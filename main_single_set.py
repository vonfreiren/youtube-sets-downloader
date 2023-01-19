import os

import yaml

from calculation.conversion import convert

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path']
path_delete_mp4 = data['path_delete_mp4']
destination = path + "/"
list_values = []




if __name__ == '__main__':
    url_1 = "https://www.youtube.com/watch?v=5OYLLNbeNpE"

    convert(url_1)
