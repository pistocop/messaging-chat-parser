# Messaging parser
🎯 Library used to extract messages wrote by myself on Whatsapp and Telegram.

## 📞 Whatsapp chat parser
Extract users text from whatsapp chats and save it as unique text file.

- **Input (to provide):** _.txt_ file exported from one or more chat
- **Output:**
    - One txt file for each user in the chat provided
    - Word cloud images
- **Usage:**
    1. Export data from whatsapp as text file [link](https://faq.whatsapp.com/en/android/23756533/)
    2. Put all chats exported under `/data/chat_raw/whatsapp/`
    3. Run `whatsapp_parser.py`
    4. Check the text file under `/data/chat_parsed/`
    5. Run `word_cloud.py`
        - Italian stopwords are used
    6. Check the images under `/data/word_cloud/` 
    
## ✈ Telegram chat parser
Extract all the messages wrote by the user (and only those).

- **Usage**
    1. Do the telegram dump - [how to](https://telegram.org/blog/export-and-more)
    2. Move the `result.json` obtained under `/data/chat_raw/telegram/`
    3. Run `telegram_parser.py
    4. Check the result file `/data/chat_parsed/user-telegram.txt`