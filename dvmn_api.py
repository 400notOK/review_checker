import requests
import os
import time
import telegram
from urllib.parse import urljoin
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
    tg_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url_dvmn_query = 'https://dvmn.org/api/long_polling/'
    timestamp = time.time()
    while True:
        try:
            response_from_dvmn_api = requests.get(
                url_dvmn_query,
                headers={'Authorization': f'Token {os.getenv("DEVMAN_API_TOKEN")}'},
                params={'timestamp': timestamp}
            )
            response_from_dvmn_api.raise_for_status()
            dvmn_api_response = response_from_dvmn_api.json()

            status = dvmn_api_response.get('status')

            if status == 'found':
                new_attempt = dvmn_api_response['new_attempts'][0]
                lesson = new_attempt['lesson_title']
                is_negative = new_attempt['is_negative']
                timestamp = dvmn_api_response['last_attempt_timestamp']
                lesson_url = dvmn_api_response["new_attempts"][0]["lesson_url"]

                if is_negative:
                    bot.send_message(
                        chat_id=tg_chat_id,
                        text=f'''
                         Преподаватель проверил работу!
                         «{lesson}»
                         Ссылка на урок: {urljoin('https://dvmn.org/', lesson_url)}
                         
                         Нужно внести правки по ревью!
                    ''')
                else:
                    bot.send_message(
                        chat_id=tg_chat_id,
                        text=f'''
                        Преподаватель проверил работу!
                        «{lesson}»
                        Ссылка на урок: {urljoin('https://dvmn.org/', lesson_url)}
                        
                        Код идеален, можно делать следующий урок!
                        ''')

                timestamp = dvmn_api_response.get('last_attempt_timestamp')
            if status == 'timeout':
                timestamp = dvmn_api_response.get('timestamp_to_request')
        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    main()
