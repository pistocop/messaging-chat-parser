import sys
import argparse
import parse
from typing import List, Dict, Tuple
from os import path

from src.utils import get_dir_files


def parse_line(line: str) -> Tuple[str, str]:
    actor = 'invalid'
    text = ''
    line_elements = parse.parse("{date}, {time} - {actor}: {text}", line)
    if line_elements:
        actor = line_elements['actor']
        text = line_elements['text']
    return actor, text


def parse_chat(file_path: str) -> Dict[str, List[str]]:
    actors_txt = {}

    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            actor, text = parse_line(line)
            actors_txt.setdefault(actor, []).append(text)
    invalid_lines = actors_txt.get('invalid', [])
    print(f'Found {len(invalid_lines)} invalid lines:\n{invalid_lines}\n')
    actors_txt.pop('invalid', None)
    return actors_txt


def save_actors_text(actors_text: Dict[str, List[str]], file_name: str, output_path: str):
    for actor, texts in actors_text.items():
        output_file = path.join(output_path, f"{actor}-{file_name}")
        print(f'Saving {output_file}')
        with open(output_file, "w") as f:
            f.writelines("\n".join(texts))


def run(chats_path: str, output_path: str):
    txt_files_name, txt_files_paths = get_dir_files(chats_path)
    print(f"Found {len(txt_files_paths)} txt files in `{chats_path}` folder: {txt_files_paths}")

    for file_name, file_path in zip(txt_files_name, txt_files_paths):
        actors_text = parse_chat(file_path)
        save_actors_text(actors_text, file_name, output_path)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--chats_path', type=str, required=False, default="../data/chat_raw/whatsapp/")
    parser.add_argument('--output_path', type=str, required=False, default="../data/chat_parsed/")
    params = parser.parse_args(argv)
    run(params.chats_path, params.output_path)


if __name__ == '__main__':
    main(sys.argv[1:])
