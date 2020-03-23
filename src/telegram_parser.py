import sys
import json
import argparse

from src.utils import extract_dict_structure


def run(json_path: str, output_path: str, chat_id_list: str = None, personal_chat: bool = None):
    telegram_data = load_data(json_path)
    usr_id = telegram_data['personal_information']['user_id']

    for chat in telegram_data['chats']['list']:
        if chat['type'] == 'saved_messages' and not personal_chat:
            pass


def load_data(json_path):
    with open(json_path, 'r') as f:
        telegram_data = json.load(f)
    telegram_data_structure = extract_dict_structure(telegram_data)
    print(f'Input json structure:\n{json.dumps(telegram_data_structure, indent=4, sort_keys=True)}')
    return telegram_data


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, required=False, default="../data/chat_raw/telegram/result.json",
                        help="Path to the json created from Telegram exporter")
    parser.add_argument('--output_path', type=str, required=False, default="../data/chat_parsed/")
    parser.add_argument('--chat_id_list', type=list, required=False, help="List of telegram chat id to export")
    parser.add_argument('--personal_chat', type=bool, required=False, default=False,
                        help="Include the telegram personal chats. Default is disabled.")
    params = parser.parse_args(argv)
    run(params.json_path, params.output_path, params.chat_id_list, params.personal_chat)


if __name__ == '__main__':
    main(sys.argv[1:])
