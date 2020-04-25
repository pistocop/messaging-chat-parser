# Messaging parser
🎯 Library used to extract messages wrote by myself on Whatsapp and Telegram.

## 📞 Whatsapp chat parser
Extract users text from whatsapp chats and save it as unique text file.

- **Input (to provide):** 
    - _.txt_ file exported from one or more chat
    - Your user name on the chat, e.g. from one line:<br> 
     _12/12/19, 08:40 - `<user_name>`: bla bla bla_ 
- **Output:**
    - One txt file with all text of user specified
    - One txt file with all text of chats, with this form:
        - _[me] bla bla bla_ for messages wrote by the `<user_name>`
        - _[other] bla bla bla_ for messages not wrote by the `<user_name>`
    - Word cloud images (only 4 curiosity)
- **Usage:**
    1. Export data from WhatsApp as text file [link](https://faq.whatsapp.com/en/android/23756533/)
    2. Put all chats exported under `/data/chat_raw/whatsapp/`
    3. Run the script from main folder <br>
        `python src/whatsapp_parser.py --user_name XXXX`
    4. Check the text file under `/data/chat_parsed/`
        - [optional] Check the lines not processed under `./tmp/`
    5. [optional] Run `word_cloud.py`
        - Italian stopwords are used
    6. Check the images under `/data/word_cloud/` 
    
## ✈ Telegram chat parser
Extract all the messages wrote by the user (and only those).

- **Usage**
    1. Do the telegram dump - [how to](https://telegram.org/blog/export-and-more)
    2. Move the `result.json` obtained under `/data/chat_raw/telegram/`
    3. Run `telegram_parser.py
    4. Check the result file `/data/chat_parsed/user-telegram.txt`
    
## 📝 Todo
- Save a file with `[me]` and `[others]` placeholder (like WhatsApp parser)
- Review of this readme 