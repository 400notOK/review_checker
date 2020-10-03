import requests
import json
import telegram
import os
from urllib.parse import urljoin
from dotenv import load_dotenv
load_dotenv()

bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
TOKEN = dict(Authorization=f'Token {os.getenv("DEVMAN_API_TOKEN")}')
URL = 'https://dvmn.org/api/long_polling/'
CHAT_ID = os.getenv('CHAT_ID')
timestamp = None

while True:
    try:
        query = requests.get(URL, headers=TOKEN, params=dict(timestamp=timestamp)).json()
        query_output = json.dumps(query, ensure_ascii=False, sort_keys=True, indent=4)
        print(query_output)
        timestamp = query.get('timestamp_to_request')
        if query['status'] == 'found':
            bot.send_message(
                chat_id=CHAT_ID,
                text=f'Преподаватель проверил работу! \n'
                     f'«{query["new_attempts"][0]["lesson_title"]}»\n'
                     f'Ссылка на урок: {urljoin("https://dvmn.org/", query["new_attempts"][0]["lesson_url"])}')

            if query["new_attempts"][0]["is_negative"] is True:
                bot.send_message(chat_id=CHAT_ID, text='Нужно внести правки по ревью!')
            else:
                bot.send_message(chat_id=CHAT_ID, text='Код идеален, можно делать следующий урок!')

            timestamp = query.get('last_attempt_timestamp')
        if query['status'] == 'timeout':
            timestamp = query.get('timestamp_to_request')
    except requests.exceptions.ReadTimeout:
        pass
    except ConnectionError:
        pass
