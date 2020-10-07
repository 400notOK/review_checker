import requests
import os
import time
import telegram
from urllib.parse import urljoin
from dotenv import load_dotenv
load_dotenv()


def main():
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')
    URL_DVM_QUERY = 'https://dvmn.org/api/long_polling/'
    timestamp = time.time()
    while True:
        try:
            query_to_dvm_api = requests.get(
                URL_DVM_QUERY,
                headers={'Authorization': f'Token {os.getenv("DEVMAN_API_TOKEN")}'},
                params={'timestamp': timestamp}
            )
            query_to_dvm_api.raise_for_status()
            json_api_response = query_to_dvm_api.json()
            if 'error' in json_api_response:
                raise requests.exceptions.HTTPError(json_api_response['error'])
            timestamp = json_api_response.get('timestamp_to_request')

            status = json_api_response.get('status')

            if status == 'found':
                new_attempts = json_api_response['new_attempts'][0]
                lesson = new_attempts['lesson_title']
                is_negative = new_attempts['is_negative']
                timestamp = json_api_response['last_attempt_timestamp']
                lesson_url = json_api_response["new_attempts"][0]["lesson_url"]

                if is_negative:
                    bot.send_message(
                        chat_id=TG_CHAT_ID,
                        text=f'''
                         Преподаватель проверил работу!
                         «{lesson}»
                         Ссылка на урок: {urljoin('https://dvmn.org/', lesson_url)}
                         
                         Нужно внести правки по ревью!
                    ''')
                else:
                    bot.send_message(
                        chat_id=TG_CHAT_ID,
                        text='''
                        Преподаватель проверил работу!
                        «{lesson}»
                        Ссылка на урок: {urljoin('https://dvmn.org/', lesson_url)}
                        
                        Нужно внести правки по ревью!
                        ''')
                    bot.send_message(chat_id=TG_CHAT_ID, text='Код идеален, можно делать следующий урок!')

                timestamp = json_api_response.get('last_attempt_timestamp')
            if status == 'timeout':
                timestamp = json_api_response.get('timestamp_to_request')
        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            time.sleep(5)
            pass


if __name__ == '__main__':
    main()
