import requests
import time
import traceback
from config import *
from VKLong import Bot
from tools.keyboards import *

from utils.tools import *

bot = Bot(token=BOT_TOKEN)

# Словари:
users = {}
action = {}

print("Стартуем!")

@bot.get_updates
def main(event):
    if event.type == "message_new":

        # Получение данных из ответа:
        message_obj = event.response['message']
        user_id = message_obj['from_id']
        message = message_obj['text'].lower()

        if user_id not in list(users.keys()):
            user_data = get_user_information(user_id)
            users[user_id] = {}
            users[user_id]['data'] = user_data
            users[user_id]['offset'] = 0
            users[user_id]['searched_profiles'] = {}
            action[user_id] = "unknown"

        if user_id in list(users.keys()):
            age = users[user_id]['data']['age']
            sex = users[user_id]['data']['sex']
            city_id = users[user_id]['data']['city_id']
            user_action = action[user_id]
            if age is None:
                if user_action == "unknown":
                    bot.answer("✍️ Введите ваш возраст:")
                    action[user_id] = "enter_age"
                else:
                    if validate_age(message):
                        users[user_id]['data']['age'] = message
                        if sex is None:
                            bot.answer("✍️ Выберите ваш пол на клавиатуре:", key_sex_choice)
                            action[user_id] = "enter_sex"
                        elif city_id is None:
                            bot.answer("✍️ Введите название вашего населенного пункта, в котором хотите найти анкеты:")
                            action[user_id] = "enter_city"
                        else:
                            action[user_id] = "null"
                            bot.answer("😺 Отлично! Теперь вы можете начать поиск анкет.", key_search)
                    else:
                        bot.answer("🤚 Ваш возраст должен быть в пределах от 18-ти до 99-ти лет!\n"
                                   "\n"
                                   "✍️ Если вы ошиблись, то повторите попытку ввода повторно:")
            elif sex is None:
                if user_action != "enter_sex":
                    bot.answer("✍️ Выберите ваш пол на клавиатуре:", key_sex_choice)
                    action[user_id] = "enter_sex"
                else:
                    if message == "мужской" or message == "женский":
                        if message == "мужской":
                            users[user_id]['data']['sex'] = 2
                        elif message == "женский":
                            users[user_id]['data']['sex'] = 1
                        if city_id is None:
                            action[user_id] = "enter_city"
                            bot.answer("✍️ Введите название вашего населенного пункта, в котором хотите найти анкеты:")
                        else:
                            action[user_id] = "null"
                            bot.answer("😺 Отлично! Теперь вы можете начать поиск анкет.", key_search)
                    else:
                        bot.answer("🤚 Вы указали недопустимый пол!\n"
                                   "\n"
                                   "✍️ Выберите ваш пол на клавиатуре:", key_sex_choice)

            elif city_id is None:
                if user_action != "enter_city":
                    action[user_id] = "enter_city"
                    bot.answer("✍️ Введите название вашего населенного пункта, в котором хотите найти анкеты:")
                else:
                    city = get_city_id(message)
                    if city:
                        users[user_id]['data']['city_id'] = city
                        action[user_id] = "null"
                        bot.answer("😺 Отлично! Теперь вы можете начать поиск анкет.", key_search)
                    else:
                        bot.answer("🤚 Нам не удалось получить информацию о указанном населенном пункте!\n"
                                   "\n"
                                   "✍️ Проверьте правильность введенного названия:", key_sex_choice)

            else:
                try:
                    if message == "🔎 поиск!":
                        bot.answer("🔎 Выполняется поиск...")
                        fetched_data = search_profiles(user_id, users)
                        bot.answer(f"💞 {fetched_data['name']}, {fetched_data['age']} | В активном поиске\n"
                                   f"Ссылка на страницу: {fetched_data['page_link']}",
                                   attachment=fetched_data['photos'])
                    else:
                        bot.answer("😺 Воспользуйся кнопкой ниже, чтобы найти подходящие анкеты!", key_search)
                except Exception as error:
                    print("Произошла ошибка:", error)
