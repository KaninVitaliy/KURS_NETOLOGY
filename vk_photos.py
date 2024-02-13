import time
import requests
import json
from pprint import pprint
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urlencode

APP_id = "51849695" # id Приложения
OATH_BASE_URL = "https://oauth.vk.com/authorize"
params = {
    "client_id": APP_id,
    "redirect_url": "https://oauth.vk.com/blank.html",
    "display": "page",
    "scope": "status,photos",
    "response_type": "token"
}

oath_url = f"{OATH_BASE_URL}?{urlencode(params)}"


class VKAPIClient:

    API_BASE_URL = "https://api.vk.com/method/"

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_profile_photos(self): # Информация о фотографиях
        params = self.get_common_params()
        params.update({"owner_id": self.user_id, "album_id": "profile"})
        response = requests.get(f'{self._build_url("photos.get")}', params=params)
        return response.json()

    def get_likes_count(self, photo_id): # Вытаскиваем информацию о лайках
        params = self.get_common_params()
        params.update({'type': 'photo', 'owner_id': self.user_id, 'item_id': photo_id})
        response = requests.get(self._build_url('likes.getList'), params=params)
        return response.json().get('response', {}).get('count', 0)



