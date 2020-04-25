"""
user_joiner.py

Script to extract all lines with `USER_TAG` from files,
and join all together in one `user-messages.txt` file.
"""
import sys
import logging
import argparse
from os.path import basename, normpath, join

from typing import List

USER_TAG = "[me]"
OTHERS_TAG = "[others]"


def run(files_directory: str, files_name: List[str], output_file: str):
    logging.info(f"files_directory:{files_directory} - files_name:{files_name}")
    user_messages = []
    for file_name in files_name:
        file_path = join(files_directory, file_name)
        file = open(file_path, 'r')
        for line in file:
            if USER_TAG in line:
                line = line.replace(USER_TAG, '')
                user_messages.append(line)
        file.close()

    logging.info(f"N° {len(user_messages)} messages found. Saving at: {output_file}")
    open(output_file, 'w').writelines(user_messages)
    logging.info("Joiner finished")


def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("--files_directory", type=str, default='./data/chat_parsed/',
                        help="path to the folder with files to parse")
    parser.add_argument("--files_name", nargs='+',
                        default=['telegram-chats.txt', 'wa-chats.txt'],
                        help="list of files name to include in the joining process")
    parser.add_argument("--output_file", type=str, default='./data/chat_parsed/user-messages.txt',
                        help="name of the output file")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args(argv[1:])
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    process_name = basename(normpath(argv[0]))
    logging.basicConfig(format=f"[{process_name}][%(levelname)s]: %(message)s", level=loglevel, stream=sys.stdout)
    delattr(args, "verbose")
    run(**vars(args))


if __name__ == '__main__':
    main(sys.argv)
