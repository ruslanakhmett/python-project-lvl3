from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import logging.config
from page_loader.logger_config import configuring_dict


logging.config.dictConfig(configuring_dict)
logger = logging.getLogger('app_logger')


CHUNK_SIZE = 128


def get_response(url, content_type='text'):  # noqa: C901
    try:  # noqa: WPS229
        response = requests.get(url)
        response.raise_for_status()  # проверяется успешность ответа, если плохой ответ то выпадет исключение
    except requests.exceptions.ConnectionError as err:
        logger.exception(err)
        raise SystemExit('Connection error! Check your network connection and try again.')

    except requests.exceptions.HTTPError as err:
        logger.exception(err)
        raise SystemExit(err)

    except requests.exceptions.RequestException as err:
        logger.exception(err)
        raise SystemExit(f'Something went wrong while loading page: {url}')

    if content_type == 'text':
        return response.text
    if content_type == 'content':
        return get_chunk(response)


def get_soup(page_url):
    html = get_response(page_url)
    return BeautifulSoup(html, 'html.parser')


def get_chunk(response):
    try:
        yield from response.iter_content(chunk_size=CHUNK_SIZE)
    except requests.exceptions.RequestException as err:
        logger.exception(err)
        raise SystemExit(f'Can not download resource {response.url}')


def get_url_from_local_link(page_url, link):
    scheme = urlparse(page_url).scheme
    netloc = urlparse(page_url).netloc
    path = urlparse(link).path
    return f'{scheme}://{netloc}{path}'


def is_local_resource(page_url, link):  # поверяем ссылки на то что они являются ссылками на локальные ресурсы типа /search/opensearch.xml либо полными ссылками с указанием того же домена полностью
    link_netloc = urlparse(link).netloc
    page_netloc = urlparse(page_url).netloc
    if link_netloc == page_netloc or not link_netloc:
        return True
    return False
