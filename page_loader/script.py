import requests
import os
from urllib.parse import urlparse


URL = 'https://ru.hexlet.io/courses'


def get_file_name(url: str):
    unpacked_url = urlparse(url)
    converted_char_to_list = list(unpacked_url.netloc + unpacked_url.path)
    replaced_list = [item if item.isalpha() or item.isdigit() else '-' for item in converted_char_to_list]
    return ''.join(replaced_list) + '.html'


def get_folder_name(url: str):
    unpacked_url = urlparse(url)
    converted_char_to_list = list(unpacked_url.netloc + unpacked_url.path)
    replaced_list = [item if item.isalpha() or item.isdigit() else '-' for item in converted_char_to_list]
    return ''.join(replaced_list) + '_files'


def get_save_path(path=os.getcwd()): # по умолчанию используется текущая папка
    return os.path.join(path, '')


def donwload(url: str, path: str):
    response = requests.get(url)
    path_to_saved_file = path + get_file_name(url)
    with open(path_to_saved_file, 'wb') as file: # wb - окрывает чтение/запись как бинарный
        file.write(response.content)
    return path_to_saved_file

print(donwload(URL, get_save_path()))