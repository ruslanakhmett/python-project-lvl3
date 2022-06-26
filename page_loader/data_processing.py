from progress.bar import Bar
import logging.config
from page_loader import names_processing, paths_processing, url_processing
from page_loader.logger_config import configuring_dict


logging.config.dictConfig(configuring_dict)
logger = logging.getLogger('app_logger')

resources_tags = {'link', 'script', 'img'}  # искомые тэги
required_attributes = {'src', 'href'}  # обзательные атрибуты


def change_local_links(page_url, soup, path_to_resource_dir):  # передаем исходную ссылку, объект супа, пусть к локальной папке с ресурсами
    logger.info('Start link search')
    tags = soup.find_all(resources_tags)  # находим все нужные теги
    for tag in tags:  # идем по тегам
        attr_and_value = get_link(tag.attrs, required_attributes)  # формируем кортежи типа ('href', '/search/opensearch.xml')
        if attr_and_value:  # если находим, разбираем по переменным
            attr, link = attr_and_value
            if url_processing.is_local_resource(page_url, link):
                logger.debug(f'Resource tag: {tag}')
                logger.debug(f'Required attribute {attr} and its value: {link}')
                resource_url = url_processing.get_url_from_local_link(page_url, link)  # формируем ссылку на ресурс из локальной в полную
                resource_file_name = names_processing.get_file_name(page_url, resource_url)  # формируем имя для сохраняемого файла
                logger.debug(f'Resource file name OK: {resource_file_name}')
                resource_path = paths_processing.make_path(path_to_resource_dir, resource_file_name)  # формируем путь для сохранения файла
                logger.debug(f'Resource path OK: {resource_path}')
                resource_content = url_processing.get_response(resource_url, content_type='content')  # запрос на скачивание контента
                logger.debug(f'Resource content OK: {resource_file_name}')
                save_content(resource_path, resource_file_name, resource_content)  # сохраняем контент
                logger.debug('Saving resource in file OK')
                tag[attr] = paths_processing.make_path_to_soup_link(resource_path)  # подменяем ссылку в html на ссылку на скачанный ресурс, сформировав его нужным образом test-com_files/test-com-courses.html
                logger.debug(f'Local link OK: {tag[attr]}')
    return soup.prettify()  # форматтер Метод prettify() превратит дерево синтаксического анализа Beautiful Soup в хорошо отформатированную строку Unicode с отдельной строкой для каждого тега и каждой строки:


def get_link(tag_attrs: dict, required_attrs: set):
    for attr, value in tag_attrs.items():
        if attr in required_attrs:  # идем по всем тегам/атрибутам, и если среди них находится нужный нам {'src', 'href'}, то берем его название и содержимое
            return attr, value


def save_content(path_to_file, resource_file_name, resource_content):  # сохранняем контент

    bar = Bar(f'{resource_file_name}', fill='@', suffix='%(percent).1d%%')

    try:
        with open(path_to_file, 'wb') as file:
            for chunk in resource_content:
                file.write(chunk)
                file.flush()  # Метод flush() в обработке файлов Python очищает внутренний буфер файла.
                bar.next()
            bar.finish()
    except OSError as err:
        logger.exception(err)
        raise OSError()


def save_page(path_to_file, resource_content):  # сохраняем html страницу
    try:
        with open(path_to_file, 'w') as file:
            file.write(resource_content)
    except OSError as err:
        logger.exception(err)
        raise OSError()
