import requests
import os
import json
import time
from progress.bar import Bar


id = '733255838'
token_vk = ''
token_yandex = ''

class Downloads_Photo:
    def __init__(self, user_id: str, token_vk: str):
        self.user_id = user_id
        self.token_vk = token_vk
        self.direct = r'D:\PhotoVk'

    def downloads_photo_from_vk(self):
        os.chdir(self.direct)
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': self.token_vk
        }
        res = requests.get(url_vk, params=params_vk)
        bar = Bar('Скачивание фото', max=len(res.json()['response']['items']))
        list_name_fils_by_likes = []
        for i in res.json()['response']['items']:
            list_name_fils_by_likes.append(i['likes']['count'])
            url_photo = i['sizes'][-1]['url']
            self.size = i['sizes'][-1]['type']
            response = requests.get(url_photo)
            for name in list_name_fils_by_likes:
                continue
            with open(f"{name}.jpg", "wb") as f:
                f.write(response.content)
                bar.next()
                time.sleep(1)
            logs_list = []
            download_log = {'file_name': name, 'size': self.size}
            logs_list.append(download_log)
            with open(f'{self.direct}/log.json', 'a') as file:
                json.dump(logs_list, file, indent=2)

if __name__ == '__main__':
    user1 = Downloads_Photo(id, token_vk)
    user1.downloads_photo_from_vk()


class Upload_Photo:
    def __init__(self, token_yandex: str):
        self.token_yandex = token_yandex
        self.direct = r'D:\PhotoVk'
        self.number_of_files_to_send = 5

    def uploading_files_to_yandex_disk(self, path):
        os.chdir(self.direct)
        files_list = [name for name in os.listdir(self.direct) if name.endswith(".jpg")]
        bar = Bar('Загрузка файлов на Я.Диск', max=len(files_list))
        count = 0
        number_of_sent = 0
        for name_file in files_list:
            count += 1
            while count <= self.number_of_files_to_send:
                number_of_sent += 1
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token_yandex}'
                }
                params = {
                    'path': f'{path}/{name_file}',
                    'overwrite': True
                }
                upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                response = requests.get(upload_url, headers=headers, params=params)
                href = response.json().get("href", "")
                response = requests.api.put(href, data=open(name_file, 'rb'), headers=headers)
                bar.next()
                time.sleep(0.5)
                break
        
    def creating_a_new_folder_on_yandex_disk(self, name_folder: str):
        headers = {
            "Accept": 'application/json',
            'Authorization': f'OAuth {self.token_yandex}'
        }
        params = {
            'path': f'/{name_folder}',
        }
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        requests.put(upload_url, headers=headers, params=params)
        return name_folder

if __name__ == '__main__':
    user = Upload_Photo(token_yandex)
    user.uploading_files_to_yandex_disk(user.creating_a_new_folder_on_yandex_disk)