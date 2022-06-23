import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pathlib
import re
import os


def make_path(path: str, path_component: str):
    if pathlib.Path(path).exists():
        return pathlib.Path(f'{path}/{path_component}')
    raise RuntimeError(
        f"The path or folder '{path}' does not exist!")


def make_path_to_soup_link(path):
    parts = pathlib.Path(path).parts
    return pathlib.Path(parts[-2]) / parts[-1]


def make_dir(output_path: str, path_component: str) -> str:
    path_to_directory = make_path(
        output_path,
        path_component)
    try:
        pathlib.Path(path_to_directory).mkdir(exist_ok=True)

    except OSError as error:
        raise RuntimeError(
            f"Unable to create directory '{path_to_directory}'",
        ) from error
    return path_to_directory


def get_name(page_url, link=False, directory=False):  # noqa: WPS210
    """Get a file or directory name from page URL.
    Returns a pair (name, extension) if you want to get the file name
    or just name if you want to get the name of the directory
    (directory=True)
    """
    domain_name = urlparse(page_url).netloc
    if link:
        root, extension = os.path.splitext(link)
        path_parts = urlparse(root).path
        extension = '.html' if extension == '' else extension
    else:
        path_parts = urlparse(page_url).path
        extension = '.html'
    name = '{0}{1}'.format(domain_name, path_parts.rstrip('/'))
    if directory:
        return convert_name(name)
    return convert_name(name), extension


def convert_name(resource):
    return re.sub(r'\W', '-', resource)


def get_file_name(page_url, source_link=False):
    return '{0}{1}'.format(*get_name(page_url, link=source_link))


# def get_folder_name(url: str):
#     unpacked_url = urlparse(url)
#     converted_char_to_list = list(unpacked_url.netloc + unpacked_url.path)
#     replaced_list = [item if item.isalpha() or item.isdigit() else '-' for item in converted_char_to_list]
#     return ''.join(replaced_list) + '_files'

def get_folder_name(url):
    return '{0}{1}'.format(get_name(url, directory=True), '_files')