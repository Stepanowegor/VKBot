import requests
import datetime
from config import *
from databases.db import *

current_year = datetime.datetime.now().year

def get_user_information(user_id):
    response = requests.get("https://api.vk.com/method/users.get",
                            params={
                                "user_ids": user_id,
                                "fields": "sex, bdate, city",
                                "access_token": BOT_TOKEN,
                                "v": 5.131
                            }).json()
    user_object = response["response"][0]

    age = None
    city_id = None
    sex = None

    try:
        if "bdate" in list(user_object.keys()):
            if len(user_object['bdate'].split(".")) == 3:
                age = current_year - int(user_object['bdate'].split(".")[-1])

        if "city" in list(user_object.keys()):
            city_id = user_object['city']['id']

        if "sex" in list(user_object.keys()):
            if user_object['sex'] > 0:
                sex = user_object['sex']

        return {"age": age,
                "city_id": city_id,
                "sex": sex}
    except KeyError:
        print("That keys does not exist!")
        return None, None, None

def validate_age(age):
    try:
        if 18 <= int(age) <= 99:
            return True
        else:
            return False
    except KeyError:
        return False

def get_city_id(name):
    response = requests.get("https://api.vk.com/method/database.getCities",
                            params={
                                "country_id": 1,
                                "q": name,
                                "count": 10,
                                "access_token": USER_TOKEN,
                                "v": 5.131
                            }).json()
    try:
        city = response['response']['items'][0]['id']
        return city
    except KeyError:
        return False


def get_popular_photos(user_id):
    response = requests.get("https://api.vk.com/method/photos.getAll",
                                params={
                                    "owner_id": user_id,
                                    "extended": 1,
                                    "count": 50,
                                    "access_token": USER_TOKEN,
                                    "v": 5.131
                                }).json()['response']
    try:
        photos_count = len(response['items'])
        if photos_count >= 3:
            likes = {}
            popular_photo = ""
            for i in range(photos_count):
                try:
                    likes_count = response['items'][i]['likes']['count']
                    likes[likes_count] = f"photo{user_id}_{response['items'][i]['id']}"
                except ValueError:
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


def search_profiles(user_id, users):
    while True:
        if users[user_id]['searched_profiles'] == {}:
            age = int(users[user_id]['data']['age'])
            offset = int(users[user_id]['offset'])
            preferred_sex = None
            if users[user_id]['data']['sex'] == 1:
                preferred_sex = 2
            elif users[user_id]['data']['sex'] == 2:
                preferred_sex = 1
            response = requests.get("https://api.vk.com/method/users.search",
                                    params={
                                        "sort": 0,
                                        "offset": offset,
                                        "count": 50,
                                        "fields": "bdate",
                                        "city_id": users[user_id]['data']['city_id'],
                                        "sex": preferred_sex,
                                        "status": 6,
                                        "age_from": age - 5,
                                        "age_to": age + 5,
                                        "has_photo": 1,
                                        "access_token": USER_TOKEN,
                                        "v": 5.131
                                    }).json()['response']['items']

            not_closed_profiles = [person for person in response if not person['is_closed']]
            users[user_id]['offset'] = offset + 50
            users[user_id]['searched_profiles'] = not_closed_profiles

        if users[user_id]['searched_profiles'] != {}:
            viewed_users = profiles.execute("SELECT showed_profile_id FROM main WHERE user_id = ?", (user_id,)).fetchall()
            while True:
                s_profiles = users[user_id]['searched_profiles'][0]
                searched_id = s_profiles['id']
                if (searched_id,) not in viewed_users:
                    has_photos = get_popular_photos(searched_id)
                    if has_photos:
                        s_age = current_year - int(s_profiles['bdate'].split(".")[-1])
                        profiles.execute("INSERT INTO main(user_id, showed_profile_id) VALUES (?, ?)", (user_id, searched_id))
                        profiles_db.commit()
                        return {"page_link": f"vk.com/id{searched_id}",
                                "name": s_profiles['first_name'],
                                "age": s_age,
                                "photos": has_photos}
                users[user_id]['searched_profiles'].pop(0)



