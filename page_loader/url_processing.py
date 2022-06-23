from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


CHUNK_SIZE = 128


def get_response(url, content_type='text'):
    response = requests.get(url)
    response.raise_for_status()
    if content_type == 'text':
        return response.text
    if content_type == 'content':
        return get_chunk(response)


def get_soup(page_url):
    html = get_response(page_url)
    return BeautifulSoup(html, 'html.parser')


def get_chunk(response):
    yield from response.iter_content(chunk_size=CHUNK_SIZE)


def get_url_from_local_link(page_url, link):
    link = link.lstrip('.')
    scheme = urlparse(page_url).scheme
    netloc = urlparse(page_url).netloc
    path = urlparse(link).path
    return f'{scheme}://{netloc}{path}'


def is_local_resource(page_url, link):
    link_netloc = urlparse(link).netloc
    page_netloc = urlparse(page_url).netloc
    return link_netloc == page_netloc or not link_netloc
