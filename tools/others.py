import requests
import datetime
import traceback
from config import USER_TOKEN
from databases.db import *

offset = 0

def get_user_data(user_id):
    try:
        response = dict(requests.get("https://api.vk.com/method/users.get",
                                params={
                                    "user_ids": user_id,
                                    "fields": "bdate, city, sex",
                                    "access_token": USER_TOKEN,
                                    "v": 5.131
                                }).json()['response'][0])

        city_id = None
        city_title = None
        bdate = None
        sex_id = None

        if response.get("city") is not None:
            city_id = response['city']['id']
            city_title = response['city']['title']

        if response.get("bdate") is not None:
            bdate = response['bdate']
            # Если год рождения скрыт:
            if int(bdate.split(".")[-1]) < 12:
                bdate = None
            else:
                bdate = int(bdate.split(".")[-1])

        if response.get("sex") is not None:
            if response['sex'] > 0:
                sex_id = response['sex']

        return [city_id, city_title, bdate, sex_id]

    except:
        return None, None, None, None

def get_city_list(name):
    try:
        response = requests.get("https://api.vk.com/method/database.getCities",
                                     params={
                                         "country_id": 1,
                                         "q": name,
                                         "access_token": USER_TOKEN,
                                         "v": 5.131
                                     }).json()['response']

        if response['count'] == 0:
            return False
        else:
            return response['items'][0]['id']
    except:
        return "error"

def validate_age(message):
    try:
        age = int(message)
        if 14 <= age <= 100:
            return age
        else:
            return "error"
    except:
        return False

def validate_sex(message):
    if message == "мужской" or message == "м":
        return 2
    elif message == "женский" or message == "ж":
        return 1
    else:
        return False

def search_users(params):

    sex_choice = 0

    # Определение возраста:
    year = int(datetime.datetime.now().year)
    age_from = year - (int(params[2]) + 5)
    age_to = year - (int(params[2]) - 5)

    # Определение пола:
    if params[3] == 1:
        sex_choice = 2
    elif params[3] == 2:
        sex_choice = 1

    try:
        response = requests.get("https://api.vk.com/method/users.search",
                                params={
                                    "sort": 0,
                                    "count": 100,
                                    "city_id": params[0],
                                    "fields": "bdate, city",
                                    "sex": sex_choice,
                                    "status": 6,
                                    "age_from": age_from,
                                    "age_to": age_to,
                                    "has_photo": 1,
                                    "access_token": USER_TOKEN,
                                    "v": 5.131
                                }).json()['response']['items']

        profiles = [person for person in response if not person['is_closed']]


        return profiles

    except KeyError:
        return False

def get_popular_photos(user_id):
    try:
        response = requests.get("https://api.vk.com/method/photos.getAll",
                                params={
                                    "owner_id": user_id,
                                    "extended": 1,
                                    "count": 50,
                                    "access_token": USER_TOKEN,
                                    "v": 5.131
                                }).json()['response']
        photos_count = len(response['items'])
        if photos_count >= 3:
            likes = {}
            popular_photo = ""
            for i in range(photos_count):
                try:
                    likes_count = response['items'][i]['likes']['count']
                    likes[likes_count] = f"photo{user_id}_{response['items'][i]['id']}"
                except:
                    pass
            for x in range(3):
                try:
                    popular_photo += f'{likes[max(list(likes.keys()))]},'
                    likes.pop(max(list(likes.keys())))
                except ValueError:
                    pass
            return popular_photo[:-1]
        else:
            return False

    except KeyError:
        return False

def fetch_profiles(response, user_id, offset):
    showed_ids = profiles.execute("SELECT showed_profile_id FROM main WHERE user_id = ?", (user_id,)).fetchall()
    while True:
        total_lists = len(response)
        profile_object = response[offset]
        profile_id = profile_object['id']
        if (profile_id,) in showed_ids:
            offset += 1
        else:
            photos = get_popular_photos(profile_id)
            if photos:
                profile_age = int(datetime.datetime.now().year) - int(profile_object['bdate'].split(".")[-1])
                profile_first_name = profile_object['first_name']
                offset += 1
                profiles.execute("INSERT INTO main(user_id, showed_profile_id) VALUES (?, ?)",
                                 (user_id, profile_id))
                profiles_db.commit()
                return [
                    profile_first_name,
                    profile_age,
                    profile_id,
                    photos,
                    offset
                ]
            else:
                offset += 1
