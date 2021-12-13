import requests
import json
from PIL import Image
import io

TOKEN = ''
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
LONG_POLLING_TIMEOUT = 10


def event_loop():
    last_update_id = None
    while True:
        r = requests.get(BASE_URL + 'getUpdates',
                         params={
                             'offset': last_update_id,
                             'timeout': LONG_POLLING_TIMEOUT
                         })
        response_dict = json.loads(r.text)
        print(r.status_code)
        print(r.text)
        for upd in response_dict["result"]:
            last_update_id = upd["update_id"] + 1
            msg = upd["message"]
            chat_id = msg["chat"]["id"]
            if 'photo' in msg:
                file_id = msg['photo'][2]['file_id']
                download_photo(file_id)
            else:
                send_message(chat_id, 'Отправьте фото для окрашивания!')


def get_file_path(file_id):
    r = requests.get(BASE_URL + 'getFile', params={'file_id': file_id})
    if r.status_code == 200:
        response_dict = json.loads(r.text)
        return response_dict['result']['file_path']


def download_photo(file_id):
    file_path = get_file_path(file_id)
    if file_path is not None:
        response = requests.get(
            f'https://api.telegram.org/file/bot{TOKEN}/{file_path}')
        if response.status_code == 200:
            picture = response.content
            show_picture(picture)


def show_picture(picture_in_bytes):
    image = Image.open(io.BytesIO(picture_in_bytes))
    image.save('test.jpg')


def send_message(chat_id, message):
    requests.post(BASE_URL + 'sendMessage', params={
        "chat_id": chat_id,
        "text": message
    })


event_loop()
