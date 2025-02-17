"""
Created on Mon Feb 17 2025
@author: unixsam, jyt2018
根据图片的exif信息、视频的metadata信息, 更改它们的文件名
文件仍旧存放于原来的文件夹
"""
import os
import exifread
from pymediainfo import MediaInfo

# 支持的图片和视频文件扩展名
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.tiff', '.tif')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv')

def get_filelist(directory):
    """
    获取指定目录下所有图片和视频文件的完整路径列表。
    :param directory: 要遍历的目录路径
    :return: 包含所有图片和视频文件完整路径的列表
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS):
                file_list.append(os.path.join(root, filename))
    return file_list

def process_image_file(file_path):
    """
    处理单个图片文件, 读取EXIF信息并根据日期时间重命名文件。
    :param file_path: 图片文件的完整路径
    """
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
        if 'EXIF DateTimeOriginal' in tags:
            img_date = tags['EXIF DateTimeOriginal']
            img_date_str = img_date.values
        elif 'Image DateTime' in tags:
            img_date = tags['Image DateTime']
            img_date_str = img_date.values
        else:
            img_date = 'Noexif'
        print(f"File: {file_path}")
        print(f"Date Info: {img_date}")
        if img_date == 'Noexif':
            print('no exif found')
        else:
            new_filename = img_date_str.replace(' ', '_').replace(':', '') + os.path.splitext(file_path)[1]
            new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
            if os.path.exists(new_file_path):
                print(f"Skip renaming {file_path} as {new_file_path} already exists.")
            else:
                print(f"New Filename: {new_filename}\n")
                os.rename(file_path, new_file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_video_file(file_path):
    """
    处理单个视频文件，读取元数据信息并根据日期时间重命名文件。
    :param file_path: 视频文件的完整路径
    """
    try:
        media_info = MediaInfo.parse(file_path)
        # 显示所有的 track 信息
        print(f"\n\n---File: {file_path}")
        print("All track information:")
        for track in media_info.tracks:
            print(f"\n***Track type: {track.track_type}")
            for attr, value in track.__dict__.items():
                if not attr.startswith("_"):
                    print(f"  {attr}: {value}")
            print()

        for track in media_info.tracks:
            if track.track_type == 'Other':  # 这里根据实际情况修改 不一定是Other，可能是Video、Audio等
                date = track.encoded_date
                print(date)
                break
        else:
            date = 'No metadata date'

        print(f"Date Info: {date}")
        if date == 'No metadata date':
            print('no metadata date found')
        else:
            # 处理日期字符串，假设日期格式为 'UTC 2023-10-10 12:34:56' 这里需要根据情况修改
            date_str = date.replace(' UTC', '').replace(':', '').replace('-', '').replace(' ', '_')
            new_filename = date_str + os.path.splitext(file_path)[1]
            new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
            if os.path.exists(new_file_path):
                print(f"Skip renaming {file_path} as {new_file_path} already exists.")
            else:
                print(f"New Filename: {new_filename}\n")
                os.rename(file_path, new_file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    target_path = input("请输入要处理的目录路径: ")
    if not os.path.isdir(target_path):
        print("输入的路径不是一个有效的目录，请重新运行程序并输入正确的路径。")
    else:
        file_list = get_filelist(target_path)
        print(f"{len(file_list)} files found.")
        for file in file_list:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                process_image_file(file)
            elif file.lower().endswith(VIDEO_EXTENSIONS):
                process_video_file(file)