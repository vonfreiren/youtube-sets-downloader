import csv
import os
import re

import eyed3

# Define the directory path
directory_path = "/Volumes/GoogleDrive/My Drive/Musica Sets"

# Create an empty list to store the file names and sizes
data = []

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    print(filename)
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path) and file_path.endswith(".mp3"):
        # Get the file size
        audio = eyed3.load(file_path)
        title = audio.tag.title
        print(title)
        artist = audio.tag.artist
        album = audio.tag.album
        genre = audio.tag.genre
        year = audio.tag.getBestDate()
        if year is None:
            match = re.search(r'\b\d{4}\b', file_path)
            if match:
                year = match.group(0)
                audio.tag.best_date = year
                audio.tag.save()
        artist_album = audio.tag.artist



        # Add the file name and size to the data list
        data.append([filename, title, artist, album, genre, year, artist_album])

    for filename in os.listdir(directory_path_2):
        file_path = os.path.join(directory_path_2, filename)
        if os.path.isfile(file_path) and file_path.endswith(".mp3"):
            # Get the file size
            audio = eyed3.load(file_path)
            title = audio.tag.title
            artist = audio.tag.artist
            album = audio.tag.album
            genre = audio.tag.genre
            year = audio.tag.getBestDate()
            if year is None:
                match = re.search(r'\b\d{4}\b', file_path)
                if match:
                    year = match.group(0)
                    audio.tag.best_date = year
                    audio.tag.save()
            artist_album = audio.tag.artist

            # Add the file name and size to the data list
            data.append([filename, title, artist, album, genre, year, artist_album])

# Write the data to a CSV file
with open("files.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Title", "Artist", "Album", "Genre", "Year", "Artist_Album"])
    writer.writerows(data)

print("CSV file created successfully!")