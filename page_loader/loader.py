from page_loader import data_processing, names_processing, paths_processing, url_processing
from page_loader.logger_config import configuring_dict


def download(page_url: str, output_path: str) -> str:
    soup = url_processing.get_soup(page_url)
    path_to_file =  paths_processing.make_path(output_path, names_processing.get_file_name(page_url))
    resource_dir_name = names_processing.get_directory_name(page_url)
    path_to_resource_dir =  paths_processing.make_dir(output_path, resource_dir_name)
    print('Loading page ...\n')

    html_with_local_links = data_processing.change_local_links(page_url, soup, path_to_resource_dir)
    data_processing.save_page(path_to_file, html_with_local_links)
    return path_to_file
