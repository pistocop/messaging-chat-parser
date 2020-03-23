# Messaging parser
Some utility build to extract text from my Whatsapp and Telegram account.

## 📞 Whatsapp chat parser
Extract users text from whatsapp chats and save it as unique text file.

- **Input (to provide):** _.txt_ file exported from one or more chat
- **Output:**:
    - One txt file for each user in the chat provided
    - Word cloud images
- **Usage:**
    1. Export data from whatsapp as text file [link](https://faq.whatsapp.com/en/android/23756533/)
    2. Put all chats exported under `data/chat_raw/`
    3. Run `src/whatsapp_parser.py`
    4. Check the text file under `data/chat_parsed/`
    5. Run `src/word_cloud.py`
        - Italian stopwords are used
    6. Check the images under `data/word_cloud/` 
    
## ✈ Telegram chat parser
