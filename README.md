# README

This script allows the user to convert a list of YouTube video URLs to mp3 files, with metadata tags added to the files using the eyed3 library. The script uses the pytube and youtube-dl libraries to download the videos and extract the audio.

The script also uses the Google Images library to retrieve the cover art for the mp3 file, and the yaml library to read a configuration file containing the destination path for the downloaded files.

The script also contains a GUI that allows the user to input the video URLs and select the quality of the mp3 files.

## Dependencies
- eyed3
- pytube
- youtube-dl
- google_images
- yaml
- PyQt6

## Configuration
You need to create a config.yaml file with the following structure:

- path: "path to save the files"

-
## Usage
Run the script and enter the youtube URLs in the GUI, select the mp3 quality and click the "Convert" button. The mp3 files will be saved in the path specified in the config.yaml file and the mp4 files will be deleted in the path specified in the config.yaml file.

Note: you need to have ffmpeg installed on your system and set the path to the ffmpeg executable in the os.environ["IMAGEIO_FFMPEG_EXE"] variable before running the script.