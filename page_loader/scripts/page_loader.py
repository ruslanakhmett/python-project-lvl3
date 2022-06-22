import argparse
import os
from page_loader.page_loader_funcs import download


DEFAULT_PATH = os.path.join(os.getcwd(), '')


def get_parser():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('-o', '--output', type=str, help='Download path', default=DEFAULT_PATH,)
    parser.add_argument('url', type=str, help='URL')
    return parser


def main():
    args = get_parser().parse_args()
    try:
        path_to_saved_file = download(args.url, args.output)
    except Exception as error:
        print(error)
    print('Saved to:')
    print(path_to_saved_file)


if __name__ == '__main__':
    main()
