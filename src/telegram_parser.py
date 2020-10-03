import logging
import os
import sys
import json
import argparse
from datetime import datetime
from os.path import normpath, basename

from tqdm import tqdm

sys.path.append("./")
from src.utils.utils import extract_dict_structure, split_in_sessions

USER_TAG = "[me]"
OTHERS_TAG = "[others]"
TELEGRAM_STOP_WORDS = [word.replace('\n', '') for word in open('./data/resources/Telegram_stopwords.txt').readlines()]


def save_messages_parsed(output_path, user_messages):
    output_file = os.path.join(output_path, "telegram-chats.txt")
    with open(output_file, 'w') as f:
        [f.write(f"{msg}\n") for msg in user_messages]


def stop_word_checker(actor, invalid_lines, text):
    if type(text) != str:  # Telegram save links under 'text' key, but they are dictionary / list
        invalid_lines.append(f"[STOP_WORD] {actor} - {text}")
        return True
    for stop_word in TELEGRAM_STOP_WORDS:
        if stop_word in text:
            invalid_lines.append(f"[STOP_WORD] {actor} - {text}")
            return True
    return False


def messages_parser(personal_chat, telegram_data, session_info: dict):
    datetime_format = session_info['time_format']
    usr_id = telegram_data['personal_information']['user_id']
    usr_messages = []
    invalid_lines = []

    for chat in tqdm(telegram_data['chats']['list']):
        if chat['type'] == 'saved_messages' and not personal_chat:
            continue  # Skip personal messages
        if chat['type'] != 'personal_chat':
            continue  # Skip everything but 1 to 1 messages
        logging.info(f"Processing chat with `{chat.get('name', 'personal messages')}`")
        t_last = None
        for message in chat['messages']:
            if message['type'] == "message" and message['text']:
                t_current = datetime.strptime(message['date'], datetime_format)
                split_in_sessions(t_current,
                                  t_last,
                                  usr_messages,
                                  session_info['delta_h_threshold'],
                                  session_info['session_token'])
                t_last = t_current
                if not stop_word_checker(message['from_id'], invalid_lines, message['text']):
                    msg_prefix = USER_TAG if message['from_id'] == usr_id else OTHERS_TAG
                    usr_messages.append(f"{msg_prefix} {message['text']}")
    logging.info(f"N° {len(invalid_lines)} invalid lines found, top 5: {invalid_lines[:5]}")
    return usr_messages


def load_data(json_path):
    with open(json_path, 'r') as f:
        telegram_data = json.load(f)
    telegram_data_structure = extract_dict_structure(telegram_data)
    # logging.info(f'Input json structure:\n{json.dumps(telegram_data_structure, indent=4, sort_keys=True)}')
    return telegram_data


def run(json_path: str,
        output_path: str,
        session_token: str,
        delta_h_threshold: int,
        time_format: str,
        personal_chat: bool = None):
    session_info = {"session_token": session_token,
                    "delta_h_threshold": delta_h_threshold,
                    "time_format": time_format}

    logging.info(f"Loading telegram user data at {json_path}...")
    telegram_data = load_data(json_path)

    logging.info(f"Start parsing telegram messages...")
    user_messages = messages_parser(personal_chat, telegram_data, session_info)

    logging.info(f"Saving {len(user_messages)}^ telegram messages...")
    save_messages_parsed(output_path, user_messages)


def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('--json_path', type=str, required=False, default="./data/chat_raw/telegram/telegram_dump.json",
                        help="Path to the json created from Telegram exporter")
    parser.add_argument('--output_path', type=str, default="./data/chat_parsed/")
    parser.add_argument('--personal_chat', type=bool, default=False,
                        help="Include the telegram personal chats. Default is disabled.")
    parser.add_argument('--session_token', type=str,
                        help="Add a 'session_token' after 'delta_h_threshold' hours"
                             "are elapsed between two messages. This allows splitting in sessions"
                             "one chat based on messages timing.")
    parser.add_argument("--delta_h_threshold", type=int, default=4,
                        help="Hours between two messages to before add 'session_token'")
    parser.add_argument("--time_format", type=str, default="%Y-%m-%dT%H:%M:%S",
                        help="The Telegram format timestamp. Default is Italian format.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args(argv[1:])
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    process_name = basename(normpath(argv[0]))
    logging.basicConfig(format=f"[{process_name}][%(levelname)s]: %(message)s", level=loglevel, stream=sys.stdout)
    delattr(args, "verbose")
    run(**vars(args))


if __name__ == '__main__':
    main(sys.argv)
