import sys
import argparse
from os.path import join
from pathlib import Path

import parse
from typing import List, Dict, Tuple
from os import path

from src.utils.utils import get_dir_files

USER_TAG = "[me]"
OTHERS_TAG = "[others]"

WA_STOP_WORDS = [word.replace('\n', '') for word in open('./data/resources/WhatsApp_stopwords.txt').readlines()]


def parse_line(line: str) -> Tuple[str, str]:
    actor = 'invalid'
    text = ''
    line_elements = parse.parse("{date}, {time} - {actor}: {text}", line)
    if line_elements:
        actor = line_elements['actor']
        text = line_elements['text']
    return actor, text


def parse_chat(file_path: str, user_name: str) -> List[str]:
    chat_text = []
    invalid_lines = []
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            actor, text = parse_line(line)
            if actor == 'invalid':
                invalid_lines.append(f"{actor} - {text}")
                continue
            if stop_word_checker(actor, invalid_lines, text):
                continue
            actor = USER_TAG if actor == user_name else OTHERS_TAG
            chat_text.append(f"{actor} {text}")
    print(f'Found {len(invalid_lines)} invalid lines in {file_path}')

    open(f"./tmp/invalid_lines_{path.basename(file_path)}", 'w').writelines("\n".join(invalid_lines))
    return chat_text


def stop_word_checker(actor, invalid_lines, text):
    for stop_word in WA_STOP_WORDS:
        if stop_word in text:
            invalid_lines.append(f"[STOP_WORD] {actor} - {text}")
            return True
    return False


def save_text(text_list: List[str], output_path: str):
    print(f'Saving {output_path}')
    with open(output_path, "w") as f:
        f.writelines("\n".join(text_list))


def run(user_name: str, chats_path: str, output_path: str):
    print(f"WA_STOP_WORDS:{WA_STOP_WORDS}")
    Path("./tmp").mkdir(parents=True, exist_ok=True)
    txt_files_name, txt_files_paths = get_dir_files(dir_path=chats_path, extension_filter=".txt")
    print(f"Found {len(txt_files_paths)} txt files in `{chats_path}` folder: {txt_files_paths}")

    wa_text = []
    for file_name, file_path in zip(txt_files_name, txt_files_paths):
        file_text_parsed = parse_chat(file_path, user_name)
        wa_text.extend(file_text_parsed)

    chat_path = join(output_path, 'wa-chats.txt')
    save_text(wa_text, chat_path)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_name', type=str, required=True)
    parser.add_argument('--chats_path', type=str, required=False, default="./data/chat_raw/whatsapp/")
    parser.add_argument('--output_path', type=str, required=False, default="./data/chat_parsed/")
    params = parser.parse_args(argv)
    run(params.user_name, params.chats_path, params.output_path)


if __name__ == '__main__':
    main(sys.argv[1:])
