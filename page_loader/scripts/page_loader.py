from page_loader.page_loader_funcs import download, get_save_path


URL = 'https://ru.hexlet.io/courses'


def main():
    download(URL, get_save_path())


if __name__ == '__main__':
    main()
