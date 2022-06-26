from page_loader import data_processing, names_processing, paths_processing, url_processing


def download(page_url: str, output_path: str) -> str:  # передаем аргументы из argparse
    soup = url_processing.get_soup(page_url)  # получаем объект BeautifulSoup
    path_to_file = paths_processing.make_path(output_path, names_processing.get_file_name(page_url))  # формируем путь и имя к сохрянаемому html
    resource_dir_name = names_processing.get_directory_name(page_url)  # формируем имя папке с ресурсами
    path_to_resource_dir = paths_processing.make_dir(output_path, resource_dir_name)  # формируем путь к папке с ресурсами
    print('Loading page ...\n')

    html_with_local_links = data_processing.change_local_links(page_url, soup, path_to_resource_dir)  # получаем измененный html с исправленными ссылками
    data_processing.save_page(path_to_file, html_with_local_links)  # сохраняем итоговый html
    return path_to_file
