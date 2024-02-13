from urllib.parse import urlencode
import requests
import json
from pprint import pprint
import vk_photos as vk_photos
import ya_save_photo as ya_save_photo
import datetime
import os

with open("token.json", "r") as file: # Открываем файл и записываем токен яндекс диска в переменную
    token_ya = json.load(file)["ya_token"]
with open("token.json", "r") as file: # Открываем файл и записываем токен ВК в переменную
    token_vk = json.load(file)["vk_token"]
date_now = datetime.datetime.now().time()
status_photo = {
    "file_name" : [],
    "size": ["z"]
    }
with open("logs/log.txt", "a", encoding="utf-8") as file:
    file.write(f"{date_now} Вход в программу")
    file.write(f"\n")
print("Добро пожаловать")

print("Введите свой id Вконтакте")
ID_VK = int(input())

with open("logs/log.txt", "a", encoding="utf-8") as file:
    file.write(f"{date_now} Клиент ввел свой id")
    file.write(f"\n")
vk_client = vk_photos.VKAPIClient(token_vk, ID_VK) # Сохранили в класс Токен и ID ВК
with open("logs/log.txt", "a", encoding="utf-8") as file:
    file.write(f"{date_now} Сохранили в класс Токен и ID ВК")
    file.write(f"\n")
photos_info = vk_client.get_profile_photos() # Получили информацию о фотографиях
with open("logs/log.txt", "a", encoding="utf-8") as file:
    file.write(f"{date_now} Получили информацию о фотографиях")
    file.write(f"\n")
ya_client = ya_save_photo.YA_APICLIENT(token_ya)
with open("logs/log.txt", "a", encoding="utf-8") as file:
    file.write(f"{date_now} Записали Яндекс Токен")
    file.write(f"\n")

if os.path.exists("Photo"):
    pass
else:
    os.mkdir("Photo")
def save_photo(photos_info): # Сохранение фотографий в папку Фото
    if photos_info["response"]["count"] <= 5: # Проверка сколько фото хранится если меньше или равно 5ти выгружаем все
        count = 0
        with open("logs/log.txt", "a", encoding="utf-8") as file:
            file.write(f"{date_now} Фотографий меньше или равно 5-ти")
            file.write(f"\n")
        count_copy = 0
        for i in range(photos_info["response"]["count"]):
            url_image = photos_info["response"]["items"][i]["sizes"][-1]["url"]
            response = requests.get(url_image)
            likes_count = vk_client.get_likes_count(photos_info["response"]["items"][i]["id"])
            if os.path.isfile(f"Photo/{likes_count}.jpg"):
                count_copy += 1
                with open(f"Photo/{likes_count}(copy-{count_copy}).jpg", "wb") as file:  # Сохранение файлов в фото
                    file.write(response.content)
                    status_photo["save_photo"].append(f"{likes_count}(copy).jpg")
            else:
                with open(f"Photo/{likes_count}.jpg", "wb") as file:  # Сохранение файлов в фото
                    file.write(response.content)
                    status_photo["file_name"].append(f"{likes_count}.jpg")
            with open("save_photo.json", "w") as file_status: # Запись успешно сохраненных файлов в файл JSON
                json.dump(status_photo, file_status)
            with open("logs/log.txt", "a", encoding="utf-8") as file:
                file.write(f"{date_now} Запись успешно сохраненных файлов в файл JSON")
                file.write(f"\n")
            if response.status_code == 200:
                count += 1
                if count == photos_info["response"]["count"]:
                    print("Все фотографии сохранены в папку Photo")
    else:
        with open("logs/log.txt", "a", encoding="utf-8") as file:
            file.write(f"{date_now} Фотографий больше 5-ти")
            file.write(f"\n")
        count = 0
        count_copy = 0
        for i in range(5): # Проверка сколько фото если больше 5ти выгружаем 5
            url_image = photos_info["response"]["items"][i]["sizes"][-1]["url"]
            response = requests.get(url_image)
            likes_count = vk_client.get_likes_count(photos_info["response"]["items"][i]["id"])
            if os.path.isfile(f"Photo/{likes_count}.jpg"):
                count_copy += 1
                with open(f"Photo/{likes_count}(copy-{count_copy}).jpg", "wb") as file:  # Сохранение файлов в фото
                    file.write(response.content)
                    status_photo["file_name"].append(f"{likes_count}(copy-{count_copy}).jpg")
            else:
                with open(f"Photo/{likes_count}.jpg", "wb") as file:  # Сохранение файлов в фото
                    file.write(response.content)
                    status_photo["file_name"].append(f"{likes_count}.jpg")
            with open("save_photo.json", "w") as file_status: # Запись успешно сохраненных файлов в файл JSON
                json.dump(status_photo, file_status)
            if response.status_code == 200:
                count += 1
                if count == 5:
                    print("Все фотографии сохранены в папку Photo")
    with open("logs/log.txt", "a", encoding="utf-8") as file:
        file.write(f"{date_now} Список фотографий записались в файл JSON")
        file.write(f"\n")

def save_photo_disk(photos_info): # Сохраняем фото на яндекс диск
    with open("save_photo.json", "r") as file_save:
        spisok_photo = json.load(file_save)["file_name"]
        name_folder = "Photo"
        ya_client.creat_folder_ya_disk(name_folder) # Создание Папки на яндекс диске
        for file in spisok_photo: # Загрузка в папку фотографии
            url_upload = ya_client.response_file_upload(name_folder, file) # Запрос файла
            with open(f"Photo/{file}", "rb") as f:
                response = requests.put(url_upload, files={"file": f})
    with open("save_photo.json", "w") as file_status:  # Запись успешно сохраненных файлов в файл JSON
        json.dump(status_photo, file_status)
    with open("logs/log.txt", "a", encoding="utf-8") as file:
        file.write(f"{date_now} Фоторафии загружены в Яндекс Диск")
        file.write(f"\n")
    print("Фотографии загружены в Яндекс Диск")


save_photo(photos_info) # Сохранили фотографии в папку Фото
save_photo_disk(photos_info) # Сохранили фотографии на яндекс диск
with open("save_photo.json", "r") as file:
    spisok = []
    INFO_PROGRAM = json.load(file)
    spisok.append(INFO_PROGRAM)
with open("save_photo.json", "w") as file:
    file.write(str(spisok))
    print(spisok)


