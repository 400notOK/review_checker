# Review checker for dvmn tasks

Telegram bot for sending notifications about verification of works on [dvmn.org](https://dvmn.org/modules).
### How to install

Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Create .env file with environment variables:
```
DEVMAN_API_TOKEN=<DEVMAN_API_TOKEN>
TELEGRAM_TOKEN=<TELEGRAM_TOKEN>
TELEGRAM_CHAT_ID=<TELEGRAM_CHAT_ID>
```

### Usage
```
python main.py
```

### Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org)
 
