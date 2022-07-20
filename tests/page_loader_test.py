import tempfile
import requests_mock
import pytest
import os
import filecmp
from page_loader.names_processing import get_file_name, get_directory_name
from page_loader.url_processing import get_response, get_url_from_local_link
from page_loader.data_processing import save_content
from page_loader import download


TEST_URL = 'https://ru.hexlet.io/courses'
FILE_NAME = 'ru-hexlet-io-courses.html'
DIRECTORY_NAME = 'ru-hexlet-io-courses_files'
URL_TO_TEST_IMAGE = 'https://rossaprimavera.ru/static/files/444af5503827.jpg'
PATH_TO_COMPARED_IMAGE = 'tests/fixtures/test_img.jpeg'


def test_get_file_name():
    assert FILE_NAME == get_file_name(TEST_URL)


def test_get_directory_name():
    assert DIRECTORY_NAME == get_directory_name(TEST_URL)


def test_lite_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get('http://test.com', text='test_page_data')
            file_path = download('http://test.com', tmp_dir)
            with open(file_path, 'r') as file:
                page = file.read()
                assert page == 'test_page_data\n'


"""Здесь декоратор @parametrize определяет три различных кортежа (link, correct_value),
так что функция test_get_url_from_local_link будет работать три раза, используя их по очереди"""


@pytest.mark.parametrize('link, correct_value',
                       [('/assets/application.css', 'https://ru.hexlet.io/assets/application.css'),
                        ('/courses', 'https://ru.hexlet.io/courses'),
                        ('/assets/professions/nodejs.png', 'https://ru.hexlet.io/assets/professions/nodejs.png')])
def test_get_url_from_local_link(link, correct_value):
    assert get_url_from_local_link(TEST_URL, link) == correct_value


# тестируем сохранение контента на примере картинки
def test_save_content():
    with tempfile.TemporaryDirectory() as tmp_dir:
        image = get_response(URL_TO_TEST_IMAGE, content_type='content')
        path_to_image = os.path.join(tmp_dir, 'test.jpg')
        save_content(path_to_image, 'test.jpg', image)

        assert os.path.isfile(path_to_image)  # является ли путь файлом
        assert filecmp.cmp(path_to_image, PATH_TO_COMPARED_IMAGE, shallow=True)  # (поверхностный) оба файла одинакового типа
        assert filecmp.cmp(path_to_image, PATH_TO_COMPARED_IMAGE, shallow=False)  # файлы имеют одинаковое содержимое


"""Функция cmp() модуля filecmp сравнивает файлы
с именами f1 и f2 и возвращает True, если их сигнатуры os.stat() равны, иначе возвращает False.
Если значение shallow=True, то файлы с одинаковыми сигнатурами os.stat() считаются равными.
При аргументе shallow=False дополнительно сравнивается содержимое файлов."""


"""тестируем полное скачивание, берем фикстуры из conftest.py, мокаем необходимые ссылки и проверяем"""


def test_download(test_html, expect_test_html):
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
