import pathlib


def make_dir(output_path: str, path_component: str) -> str:
    path_to_directory = make_path(output_path, path_component)
    pathlib.Path(path_to_directory).mkdir(exist_ok=True)  # создает каталог и не вызывает исключения, если каталог уже существует.exist_ok
    return path_to_directory


def make_path(path: str, path_component: str) -> str:
    if pathlib.Path(path).exists():  # проверяет, что путь существует
        return pathlib.Path(f'{path}/{path_component}')  # возвращаем сконструированный путь


def make_path_to_soup_link(path: str) -> str:
    parts = pathlib.Path(path).parts  # parts раскладывает весь путь на кортеж элементов ('/', 'usr', 'bin', 'python3')
    return pathlib.Path(parts[-2]) / parts[-1]  # и собираем путь из двух последних элементов
