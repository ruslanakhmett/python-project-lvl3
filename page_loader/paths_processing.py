import pathlib


def make_dir(output_path: str, path_component: str) -> str:
    path_to_directory = make_path(output_path, path_component)
    pathlib.Path(path_to_directory).mkdir(exist_ok=True)
    return path_to_directory


def make_path(path: str, path_component: str) -> str:
    if pathlib.Path(path).exists():
        return pathlib.Path(f'{path}/{path_component}')
        

def make_path_to_soup_link(path):
    parts = pathlib.Path(path).parts
    return pathlib.Path(parts[-2]) / parts[-1]
