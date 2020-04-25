📲 📩 📫 ✏ 🖊 Messaging parser
================================================================================

*Use what you had written*

## What is this repo?
This repository provides python scripts to parse WhatsApp and Telegram messages.<br>
The goal is to obtain text files with a good structure for machine learning purposes. [4]

## 📥 Inputs
Data to provide:
- WhatsApp data
    - _.txt_ files exported from one or more chat - [how](https://faq.whatsapp.com/en/android/23756533/)
        - place all txt files in `./data/chat_raw/whatsapp/*.txt`
- Telegram data
    - _.json_ with the telegram dump - [how to](https://telegram.org/blog/export-and-more)
        - copy and rename the json file in `./data/chat_raw/telegram/telegram_dump.json`

## ⚙ Usage
- Install `requirements.txt`
- WhatsApp [1]
    > python ./src/whatsapp_parser.py --user_name <user_name>
- Telegram [2]
    > python ./src/telegram_parser.py
- Extract user only messages
    > python ./src/user_joiner.py

## 📤 Outputs
- `telegram-chats.txt` and `wa-chats.txt`
    - Created after scripts running inside _./data/chat_parsed/_ folder
    - Will have this structure both: <br>
    _[me] bla bla bla_ <br>
    _[others] bla bla bla_ <br>
    _[others] bla bla bla_ <br>
    _[me] bla bla bla_ <br>
    - Where the two tags:
        - `[me]`: placed as suffix of text wrote by the user [3]
        - `[others]`: placed as suffix of text wrote by others
- `user-messages.txt`
    - Created after scripts running inside _./data/chat_parsed/_ folder
    - One line per message wrote by the user [3]

----

### 📝 Notes
- [1] How find `<user_name>` value?
    -  From the WhatsApp chat exported text, e.g. from one line: <br> 
     _12/12/19, 08:40 - `<user_name>`: bla bla bla_ 
- [2] Check that the telegram dump is named `telegram_dump.json` and is inside <br>
    _./data/chat_raw/telegram/telegram_dump.json_
- [3] _user_ = the owner of the messages (I hope it coincides with who use those scripts ) 
    - the account that had done the data dump for Telegram
    - the value passed in `--user_name` in WhatsApp parser
- [4] **⚠** Is always better to don't run random scripts on personal information (like chat messages)
    - You can check this code
    - Take in mind that before:
        - This is a free-time project, I'm not guaranteeing efficiently or good programming practice
        - I'm not so good at writing English 
        - Good luck
- WhatsApp parsed isn't tested on groups exported data and is not intended to manage those types of information.
       
