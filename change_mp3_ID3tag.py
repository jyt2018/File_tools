"""
This script modifies the metadata of MP3 files in a specified directory.
It updates the title and track number based on the file name.
It also updates the artist field based on the folder name.

Author: jyt2018@github
"""

import os
import mutagen
from mutagen.easyid3 import EasyID3

def modify_mp3_meta(directory):
    """
    Modify the metadata of MP3 files in the specified directory.
    Updates the title and track number based on the file name.

    Args:
        directory (str): The directory containing MP3 files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                try:
                    audio = EasyID3(file_path)
                except mutagen.id3.ID3NoHeaderError:
                    audio = mutagen.File(file_path, easy=True)
                    audio.add_tags()
                new_title = file[3:-4]  # 从第四个字符开始到倒数第四个字符（不包括扩展名）
                audio['title'] = new_title
                track_order = file[:2]  # 文件名前两位
                album_track = track_order.lstrip('0')  # 去掉最左边的"0"
                audio['tracknumber'] = album_track
                audio.save()

def update_artist_tag(directory):
    """
    Update the artist tag of MP3 files in the specified directory based on the folder name.

    Args:
        directory (str): The directory containing MP3 files.
    """
    artist_name = os.path.basename(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                try:
                    audio = EasyID3(file_path)
                except mutagen.id3.ID3NoHeaderError:
                    audio = mutagen.File(file_path, easy=True)
                    audio.add_tags()
                audio['artist'] = artist_name
                audio.save()

def update_album_tag(directory, album_name):
    """
    Update the album tag of MP3 files in the specified directory based on user input.

    Args:
        directory (str): The directory containing MP3 files.
        album_name (str): The album name to set in the MP3 files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                try:
                    audio = EasyID3(file_path)
                except mutagen.id3.ID3NoHeaderError:
                    audio = mutagen.File(file_path, easy=True)
                    audio.add_tags()
                audio['album'] = album_name
                audio.save()
    

if __name__ == "__main__":
    # 指定要遍历的目录
    directory = r'G:\music\enigma'
    # modify_mp3_meta(directory)
    update_artist_tag(directory)
    update_album_tag(directory, "《MCMXC a.D.》")