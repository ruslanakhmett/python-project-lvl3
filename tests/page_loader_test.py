import tempfile
import requests_mock
from page_loader.page_loader_funcs import download, get_file_name, get_folder_name


TEST_URL = 'https://ru.hexlet.io/courses'
FILE_NAME = 'ru-hexlet-io-courses.html'
FOLDER_NAME = 'ru-hexlet-io-courses_files'


def test_get_file_name():
    assert FILE_NAME == get_file_name(TEST_URL)


def test_get_folder_name():
    assert FOLDER_NAME == get_folder_name(TEST_URL)


def test_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get('http://test.com', text='test_page_data')
            file_path = download('http://test.com', tmp_dir)
            with open(file_path, 'r') as file:  # noqa: WPS110
                page = file.read()
                assert page == 'test_page_data'
