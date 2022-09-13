import os
import re
from urllib.parse import urlparse


def get_name(
    page_url, link=False, directory=False
):  # передаем исходную ссылку на страницу, link and directory - типа флаги, говорят для чего мы формируем име, для файла или для папки
    domain_name = urlparse(page_url).netloc  # разбираем URL
    if link:  # если нам передана полная ссылка до файла в интернете
        root, extension = os.path.splitext(
            link
        )  # берем отдельно https://ru.hexlet.io/packs/js/runtime  и  .js
        path_parts = urlparse(
            root
        ).path  # берем только путь, без домена и без разширения файла /packs/js/runtime
        extension = (
            ".html" if extension == "" else extension
        )  # если расширения не было то делаем html, если было то берем его
    else:  # если ссылки не было
        path_parts = urlparse(page_url).path  # берем только путь, без домена /courses
        extension = ".html"
    name = "{0}{1}".format(
        domain_name, path_parts.rstrip("/")
    )  # формируем имя ru.hexlet.io/courses
    if directory:
        return convert_name(name)
    return convert_name(name), extension


def convert_name(resource):
    return re.sub(
        r"\W", "-", resource
    )  # все НЕ буквы меняем на минусы и формируем имя для папки


def get_file_name(page_url, source_link=False):
    return "{0}{1}".format(*get_name(page_url, link=source_link))


def get_directory_name(page_url):
    return "{0}{1}".format(get_name(page_url, directory=True), "_files")
