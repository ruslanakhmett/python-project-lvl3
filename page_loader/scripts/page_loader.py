import argparse
import os
import sys
from page_loader.page_loader import download
import logging.config
from page_loader.logger_config import configuring_dict


logging.config.dictConfig(configuring_dict)
logger = logging.getLogger('app_logger')

DEFAULT_PATH = os.path.join(os.getcwd(), '')


def get_parser():
    parser = argparse.ArgumentParser(usage='page-loader [-h] [-o OUTPUT] url',
                                     description='Download html page')
    parser.add_argument('-o', '--output', type=str, help='Download path', default=DEFAULT_PATH,)
    parser.add_argument('url', type=str, help='URL')
    return parser


def main():
    args = get_parser().parse_args()
    try:
        path_to_saved_file = download(args.url, args.output)
    except Exception as error:
        logger.error(error)
        print('Unexpected error! For additional info see page_loader.log')
        sys.exit(1)
    message = f'Saved to: {path_to_saved_file}'
    print(message)
    logger.info(message)
    sys.exit(0)


if __name__ == '__main__':
    main()
