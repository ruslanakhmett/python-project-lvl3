from progress.bar import Bar
from page_loader import  names_processing, paths_processing, url_processing


resources_tags = {'link', 'script', 'img'}
required_attributes = {'src', 'href'}


def change_local_links(page_url, soup, path_to_resource_dir):
    tags = soup.find_all(resources_tags)
    for tag in tags:
        attr_and_value = get_link(tag.attrs, required_attributes)
        if attr_and_value:
            attr, link = attr_and_value
            if url_processing.is_local_resource(page_url, link):
                if link.startswith('data:'):
                    continue
                resource_url = url_processing.get_url_from_local_link(page_url, link)
                resource_file_name = names_processing.get_file_name(page_url, resource_url)
                resource_path =  paths_processing.make_path(path_to_resource_dir, resource_file_name)
                resource_content = url_processing.get_response(resource_url, content_type='content')
                save_content(resource_path, resource_file_name, resource_content)
                tag[attr] =  paths_processing.make_path_to_soup_link(resource_path)
    return soup.prettify()


def get_link(tag_attrs: dict, required_attrs: set):
    for attr, value in tag_attrs.items():
        if attr in required_attrs:
            return attr, value


def save_content(path_to_file, resource_file_name, resource_content):

    bar = Bar(f'{resource_file_name}', suffix='%(percent).1d%%', color='cyan')

    with open(path_to_file, 'wb') as file:
        for chunk in resource_content:
            file.write(chunk)
            file.flush()
            bar.next()  # noqa: B305
        bar.finish()


def save_page(path_to_file, resource_content):
    with open(path_to_file, 'w') as file:
        file.write(resource_content)
