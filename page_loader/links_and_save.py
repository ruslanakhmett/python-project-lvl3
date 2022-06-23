import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pathlib
import re
import os
from page_loader.names_and_paths import get_file_name, make_path, make_path_to_soup_link


resources_tags = {'link', 'script', 'img'}
required_attributes = {'src', 'href'}

CHUNK_SIZE = 128



def get_url_from_local_link(url, link):
    """Get URL from local resources link."""
    link = link.lstrip('.')
    scheme = urlparse(url).scheme
    netloc = urlparse(url).netloc
    path = urlparse(link).path
    return f'{scheme}://{netloc}{path}'


def get_link(tag_attrs: dict, required_attrs: set):
    for attr, value in tag_attrs.items():
        if attr in required_attrs:
            return attr, value


def get_response(url, content_type='text'):

    response = requests.get(url)
    response.raise_for_status()

    if content_type == 'text':
        return response.text
    if content_type == 'content':
        return get_chunk(response)


def is_local_resource(url, link):
    link_netloc = urlparse(link).netloc
    page_netloc = urlparse(url).netloc
    return link_netloc == page_netloc or not link_netloc


def change_local_links(url, soup, path_to_resource_dir):
    tags = soup.find_all(resources_tags)
    for tag in tags:
        attr_and_value = get_link(tag.attrs, required_attributes)
        if attr_and_value:
            attr, link = attr_and_value
            if is_local_resource(url, link):
                if link.startswith('data:'):
                    continue
                resource_url = get_url_from_local_link(url, link)
                resource_file_name = get_file_name(url, resource_url)
                resource_path = make_path(path_to_resource_dir, resource_file_name)
                resource_content = get_response(url, content_type='content')
                save_content(resource_path, resource_file_name, resource_content)
                tag[attr] = make_path_to_soup_link(resource_path)
    return soup.prettify()


def get_soup(url):
    html = get_response(url)
    return BeautifulSoup(html, 'html.parser')


def save_page(path_to_file, resource_content):
    with open(path_to_file, 'w') as file:
        file.write(resource_content)


def save_content(path_to_file, resource_file_name, resource_content):
    with open(path_to_file, 'wb') as file:
        for chunk in resource_content:
            file.write(chunk)
            file.flush()


def get_chunk(response):
    try:
        yield from response.iter_content(chunk_size=CHUNK_SIZE)

    except requests.exceptions.RequestException as error:
        logger.exception(error)
        raise SystemExit(
            f'Can not download resource {response.url}',
        )
