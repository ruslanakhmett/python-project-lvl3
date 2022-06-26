import os
import re
from urllib.parse import urlparse


def get_name(page_url, link=False, directory=False):  # передаем исходную ссылку на страницу, link and directory - типа флаги, говорят для чего мы формируем име, для файла или для папки
    domain_name = urlparse(page_url).netloc  # разбираем URL
    if link:  # если формируем для файла
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


def get_directory_name(page_url):
    return '{0}{1}'.format(get_name(page_url, directory=True), '_files')
