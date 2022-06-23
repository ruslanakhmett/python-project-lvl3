import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pathlib
import re
import os
from page_loader.links_and_save import get_response, change_local_links, get_soup, save_page
from page_loader.names_and_paths import make_path, get_file_name, get_folder_name, make_dir



def download(url: str, path: str) -> str:
    soup = get_soup(url)
    path_to_file = make_path(path, get_file_name(url))
    resource_folder_name = get_folder_name(url)
    path_to_resource_dir = make_dir(path, resource_folder_name)
    print('Loading...')
    html_with_local_links = change_local_links(url, soup, path_to_resource_dir)
    save_page(path_to_file, html_with_local_links)
    return path_to_file