import sys
import logging
import argparse
import parse

from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
from os.path import join, basename, normpath

from src.utils.utils import get_dir_files, TimeFormat, split_in_sessions

USER_TAG = "[me]"
OTHERS_TAG = "[others]"

WA_STOP_WORDS = [word.replace('\n', '') for word in open('./data/resources/WhatsApp_stopwords.txt').readlines()]


def parse_line(line: str, datetime_format: str) -> Tuple[Optional[datetime], str, str]:
    timestamp = None
    actor = 'invalid'
    text = ''

    line_elements = parse.parse("{date}, {time} - {actor}: {text}", line)
    if line_elements:
        message_datetime = f"{line_elements['date']}, {line_elements['time']}"  # e.g. "31/12/19, 20:02"
        timestamp = datetime.strptime(message_datetime, datetime_format)
        actor = line_elements['actor']
        text = line_elements['text']
    return timestamp, actor, text


def stop_word_checker(actor, invalid_lines, text):
    for stop_word in WA_STOP_WORDS:
        if stop_word in text:
            invalid_lines.append(f"[STOP_WORD] {actor} - {text}")
            return True
    return False


def save_text(text_list: List[str], output_path: str):
    logging.info(f'Saving {output_path}')
    with open(output_path, "w") as f:
        f.writelines("\n".join(text_list))


def parse_chat(file_path: str,
               user_name: str,
               datetime_format: str,
               delta_h_threshold: int,
               session_token: str = None) -> List[str]:
    chat_text = [session_token] if session_token else []
    invalid_lines = []

    with open(file_path) as f:
        lines = f.readlines()
        t_last = None
        for line in lines:
            t_current, actor, text = parse_line(line, datetime_format)

            if actor == 'invalid':
                invalid_lines.append(f"{actor} - {text}")
                continue
            if stop_word_checker(actor, invalid_lines, text):
                continue

            split_in_sessions(t_current, t_last, chat_text, delta_h_threshold, session_token)
            t_last = t_current

            actor = USER_TAG if actor == user_name else OTHERS_TAG
            chat_text.append(f"{actor} {text}")
    logging.info(f'Found {len(invalid_lines)} invalid lines in {file_path}')

    open(f"./tmp/invalid_lines_{basename(file_path)}", 'w').writelines("\n".join(invalid_lines))
    return chat_text


def run(user_name: str,
        chats_path: str,
        output_path: str,
        time_format: TimeFormat,
        delta_h_threshold: int,
        session_token: str = None):
    datetime_format = "%d/%m/%y, %H:%M" if time_format == TimeFormat.world else "%m/%d/%y, %H:%M"

    logging.info(f"WA_STOP_WORDS:{WA_STOP_WORDS}")
    Path("./tmp").mkdir(parents=True, exist_ok=True)
    txt_files_name, txt_files_paths = get_dir_files(dir_path=chats_path, extension_filter=".txt")
    logging.info(f"Found {len(txt_files_paths)} txt files in `{chats_path}` folder: {txt_files_paths}")

    wa_text = []
    for file_name, file_path in zip(txt_files_name, txt_files_paths):
        file_text_parsed = parse_chat(file_path, user_name, datetime_format, delta_h_threshold, session_token)
        wa_text.extend(file_text_parsed)

    chat_path = join(output_path, 'wa-chats.txt')
    save_text(wa_text, chat_path)


def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('--user_name', type=str, required=True,
                        help="The whatsapp user name of User. It could be read on the WhatsApp raws data.")
    parser.add_argument('--chats_path', type=str, default="./data/chat_raw/whatsapp/")
    parser.add_argument('--output_path', type=str, default="./data/chat_parsed/")
    parser.add_argument('--session_token', type=str,
                        help="Add a 'session_token' after 'delta_h_threshold' hours"
                             "are elapsed between two messages. This allows splitting in sessions"
                             "one chat based on messages timing.")
    parser.add_argument("--delta_h_threshold", type=int, default=4,
                        help="Hours between two messages to before add 'session_token'")
    parser.add_argument("--time_format", type=TimeFormat, choices=list(TimeFormat), default=TimeFormat.world,
                        help="The WhatsApp datetime format, two choice: world and usa.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args(argv[1:])
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    process_name = basename(normpath(argv[0]))
    logging.basicConfig(format=f"[{process_name}][%(levelname)s]: %(message)s", level=loglevel, stream=sys.stdout)
    delattr(args, "verbose")
    run(**vars(args))


if __name__ == '__main__':
    main(sys.argv)
