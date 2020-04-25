import os
import sys
import json
import argparse
from tqdm import tqdm

from src.utils.utils import extract_dict_structure, params_printer

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


def messages_parser(personal_chat, telegram_data):
    usr_id = telegram_data['personal_information']['user_id']
    usr_messages = []
    invalid_lines = []
    for chat in tqdm(telegram_data['chats']['list']):
        if chat['type'] == 'saved_messages' and not personal_chat:
            continue  # Skip personal messages
        print(f"Processing chat with `{chat.get('name', 'personal messages')}`")
        for message in chat['messages']:
            if message['type'] == "message" and message['text']:
                if not stop_word_checker(message['from_id'], invalid_lines, message['text']):
                    msg_prefix = USER_TAG if message['from_id'] == usr_id else OTHERS_TAG
                    usr_messages.append(f"{msg_prefix} {message['text']}")
    print(f"N° {len(invalid_lines)} invalid lines found, top 5: {invalid_lines[:5]}")
    return usr_messages


def load_data(json_path):
    with open(json_path, 'r') as f:
        telegram_data = json.load(f)
    telegram_data_structure = extract_dict_structure(telegram_data)
    print(f'Input json structure:\n{json.dumps(telegram_data_structure, indent=4, sort_keys=True)}')
    return telegram_data


def run(json_path: str, output_path: str, personal_chat: bool = None):
    print(f"Loading telegram user data at {json_path}...")
    telegram_data = load_data(json_path)

    print(f"Start parsing telegram messages...")
    user_messages = messages_parser(personal_chat, telegram_data)

    print(f"Saving {len(user_messages)}^ telegram messages...")
    save_messages_parsed(output_path, user_messages)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, required=False, default="./data/chat_raw/telegram/telegram_dump.json",
                        help="Path to the json created from Telegram exporter")
    parser.add_argument('--output_path', type=str, required=False, default="./data/chat_parsed/")
    parser.add_argument('--personal_chat', type=bool, required=False, default=False,
                        help="Include the telegram personal chats. Default is disabled.")
    params = parser.parse_args(argv)
    run(params.json_path, params.output_path, params.personal_chat)


if __name__ == '__main__':
    main(sys.argv[1:])
