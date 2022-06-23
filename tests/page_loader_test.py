import tempfile
import requests_mock
import pytest
import os
import filecmp
from page_loader.names_processing import get_file_name, get_directory_name
from page_loader.url_processing import get_response, get_url_from_local_link
from page_loader.loader import download
from page_loader.data_processing import save_content


TEST_URL = 'https://ru.hexlet.io/courses'
FILE_NAME = 'ru-hexlet-io-courses.html'
DIRECTORY_NAME = 'ru-hexlet-io-courses_files'


def test_get_file_name():
    assert FILE_NAME == get_file_name(TEST_URL)


def test_get_directory_name():
    assert DIRECTORY_NAME == get_directory_name(TEST_URL)


def test_lite_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get('http://test.com', text='test_page_data')
            file_path = download('http://test.com', tmp_dir)
            with open(file_path, 'r') as file:  # noqa: WPS110
                page = file.read()
                assert page == 'test_page_data\n'


@pytest.mark.parametrize(
    'link, correct_value',
    [
        (
            '/assets/application.css',
            'https://ru.hexlet.io/assets/application.css',
        ),
        (
            '/courses',
            'https://ru.hexlet.io/courses',
        ),
        (
            '/assets/professions/nodejs.png',
            'https://ru.hexlet.io/assets/professions/nodejs.png',
        ),
    ],
)
def test_get_url_from_local_link(link, correct_value):
    assert get_url_from_local_link(TEST_URL, link) == correct_value


@pytest.mark.parametrize(
    'img_url, compared_image',
    [
        (
            (
                'https://rossaprimavera.ru/static/files/444af5503827.jpg'
            ),
            'tests/fixtures/test_img.jpeg',
        ),
    ],
)
def test_save_content(img_url, compared_image):
    with tempfile.TemporaryDirectory() as tmp_dir:
        image = get_response(img_url, content_type='content')
        path_to_image = os.path.join(tmp_dir, 'test.jpg')
        save_content(path_to_image, 'test.jpg', image)

        assert os.path.isfile(path_to_image)
        assert filecmp.cmp(path_to_image, compared_image, shallow=True)
        assert filecmp.cmp(path_to_image, compared_image, shallow=False)


def test_full_download(test_html, expect_test_html):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get('http://test.com', text=test_html)
            mocker.get('http://test.com/assets/application.css')
            mocker.get('http://test.com/courses')
            mocker.get('http://test.com/assets/professions/nodejs.png')
            mocker.get('http://test.com/packs/js/runtime.js')
            result_path = download('http://test.com', tmp_dir)
            with open(result_path, 'r', encoding='utf-8') as file:
                page = file.read()

        assert page == expect_test_html