📲 Messaging parser
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
    - _.json_ with the telegram dump - [how](https://telegram.org/blog/export-and-more) [5]
        - copy and rename the json file in `./data/chat_raw/telegram/telegram_dump.json`

## ⚙ Usage
- Install `requirements.txt`
- WhatsApp [1]
    > python ./src/whatsapp_parser.py --session_token "<|endoftext|>" --delta_h_threshold 4 --user_name **<user_name>** 
- Telegram [2]
    > python ./src/telegram_parser.py --session_token "<|endoftext|>" --delta_h_threshold 4
- Join files and extract user messages
    > python ./src/joiner.py

## 📤 Outputs
- `telegram-chats.txt` and `wa-chats.txt`
    - Will have this structure both: <br>
    _[me] bla bla bla_ <br>
    _[others] bla bla bla_ <br>
    _[others] bla bla bla_ <br>
     <|endoftext|> <br>
    _[me] bla bla bla_ <br>
     ...
    - Where the three tags:
        - `[me]`: placed as suffix of text wrote by the user [3]
        - `[others]`: placed as suffix of text wrote by others
        - `<|endoftext|>`: added when the time elapsed between two sequential messages is > 4 hours
- `all-messages.txt`
    - One file with both `telegram-chats.txt` and `wa-chats.txt` rows.
- `user-messages.txt`
    - One line per message wrote by the user [3]


----

### 📝 Notes
- [1] How find `<user_name>` value?
    -  From the WhatsApp chat exported text, e.g. from one line: <br> 
     _12/12/19, 08:40 - `<user_name>`: bla bla bla_ 
- [2] Check that the telegram dump is named `telegram_dump.json` and is inside <br>
    _./data/chat_raw/telegram/telegram_dump.json_
- [3] _user_ = the owner of the messages (I hope it coincides with who use those scripts) 
    - the account that had done the data dump for Telegram
    - the value passed in `--user_name` in WhatsApp parser
- [4] **⚠** Is always better to don't run random scripts on personal information (like chat messages)
    - You can check this code
    - Take in mind that before:
        - This is a free-time project, I'm not guaranteeing efficiently or good programming practice
        - I'm not so good at writing English 
        - Good luck
- [5] Be sure to select the "Account information" checkbox into the telegram dump dialog window
- Both Telegram and WhatsApp parsers aren't tested on the group's chats data and is not intended to manage those types of information.       
- Is possible to change the chat session behavior 
    - with `--session_token` we can change the session splitting token, if argument not provided session split will be
    disabled. 
    - with `--delta_h_threshold` is possible to change the time windows to be elapsed
    between two sequential messages before inserting a `session_token`
- 📅 Parsing data with custom values:
    - Both WhatsApp and Telegram parser use a default Italian datetime format
    - You can always use a custom format parser by using the `--time_format` parameter:
        - WhatApp:<br>
        > python ./src/whatsapp_parser.py --session_token "<|endoftext|>" --delta_h_threshold 4 --user_name **<user_name>** --time_format "%d/%m/%y, %H:%M"
        - Telegram:<br>
        > python ./src/telegram_parser.py --session_token "<|endoftext|>" --time_format "%Y-%m-%dT%H:%M:%S"
