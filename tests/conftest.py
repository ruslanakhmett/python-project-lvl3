"""Обмен Fixtures через conftest.py
Можно поместить фикстуры в отдельные тестовые файлы, но для совместного использования фикстур в нескольких
тестовых файлах лучше использовать файл conftest.py где-то в общем месте, централизованно для всех тестов
Взятые оттуда, fixtures могут быть использованы любым тестом."""

import os
import pytest

path_to_fixtures = os.path.join('tests', 'fixtures')


@pytest.fixture
def test_html():
    with open(os.path.join(path_to_fixtures, 'test_page.html')) as fixture:
        fixture_data = fixture.read()
    return fixture_data


@pytest.fixture
def expect_test_html():
    with open(os.path.join(path_to_fixtures, 'expect_test_page.html')) as fixture:
        fixture_data = fixture.read()
    return fixture_data
