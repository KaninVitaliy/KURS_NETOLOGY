import requests
import json
import vk_photos as vk_photo_ya
from pprint import pprint
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urlencode


url_yadisk = "https://cloud-api.yandex.net"
url_creat_folder = f"{url_yadisk}/v1/disk/resources"


class YA_APICLIENT:

    def __init__(self, YA_API):
        self.YA_API = YA_API
        self.headers_dict = {
            "Authorization": YA_API
        }

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }
    def creat_folder_ya_disk(self, name_folder): # Создали папку на яндекс диске
        self.params_dict = {
            "path": name_folder
        }
        self.response = requests.put(url_creat_folder,
                        params=self.params_dict,
                        headers=self.headers_dict)

    def response_file_upload(self, name_folder ,file):
        self.url_get_upload = f"{url_yadisk}/v1/disk/resources/upload"
        self.response_ya = requests.get(self.url_get_upload,
                                   headers=self.headers_dict,
                                   params={"path": f"{name_folder}/{file}"}
                                   )
        self.url_for_upload = self.response_ya.json().get("href", "")
        return self.url_for_upload


    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({"owner_id": self.user_id, "album_id": "profile"})
        response = requests.get(f'{self._build_url("photos.get")}', params=params)
        return response.json()





