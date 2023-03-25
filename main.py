import requests
import time
import traceback
from config import *
from VKLong import Bot
from tools.others import *
from tools.keyboards import *

bot = Bot(token=BOT_TOKEN)

# Переменные:
action = {}
users = {}
profiles = {}
offsets = {}

try:
    @bot.get_updates
    def main(event):
        if event.type == "message_new":

            # Получение данных из ответа:
            message_obj = event.response['message']
            user_id = message_obj['from_id']
            message = message_obj['text'].lower()

            if user_id not in list(action.keys()):
                user_data = get_user_data(user_id)
                users[user_id] = user_data

                # Если не указаны данные в профиле:
                if user_data[0] is None:
                    action[user_id] = "enter_city"
                    bot.answer("😿 Увы, но нам не удалось получить сведения о твоём месте проживания!\n"
                               "\n"
                               "👉 Укажи название своего города:")

                elif user_data[2] is None:
                    action[user_id] = "enter_age"
                    bot.answer("😿 Увы, но нам не удалось получить сведения о твоём возрасте!\n"
                               "\n"
                               "👉 Укажи свой возраст:")

                elif user_data[3] is None:
                    action[user_id] = "enter_sex"
                    bot.answer("😿 Увы, но нам не удалось получить сведения о твоём поле!\n"
                               "\n"
                               "👉 Укажи свой пол:")
                else:
                    action[user_id] = "null"
                    bot.answer("🥳 Поздравляем! Вы успешно заполнили данные и теперь можете приступать к поиску новых знакомств.", key_search)


            else:
                if action[user_id] == "enter_city":
                    city_result = get_city_list(message)
                    if city_result:
                        if city_result != "error":
                            users[user_id][0] = city_result
                            if users[user_id][2] is None:
                                action[user_id] = "enter_age"
                                bot.answer("😺 Отлично! Теперь нам нужно узнать твой возраст:")
                            elif users[user_id][3] is None:
                                action[user_id] = "enter_sex"
                                bot.answer("😺 Отлично! Нам осталось узнать твой пол:", key_sex_choice)
                            else:
                                action[user_id] = "null"
                                bot.answer("🥳 Поздравляем! Вы успешно заполнили данные и теперь можете приступать к поиску новых знакомств.", key_search)
                        else:
                            bot.answer("😿 Произошла ошибка во время получения информации о указанном городе!\n"
                                       "\n"
                                       "Попробуйте повторить ввод вашего города позднее.")
                    else:
                        bot.answer("😾 Нам не удалось получить информацию о указанном городе.\n"
                                   "\n"
                                   "Проверьте правильность введенного города и повторите попытку ввода:")
                elif action[user_id] == "enter_age":
                    age = validate_age(message)
                    if age:
                        if age != "error":
                            users[user_id][2] = age
                            if user_id[user_id][3] is None:
                                action[user_id] = "enter_sex"
                                bot.answer("😺 Отлично! Нам осталось узнать твой пол:", key_sex_choice)
                            else:
                                action[user_id] = "null"
                                bot.answer("🥳 Поздравляем! Вы успешно заполнили данные и теперь можете приступать к поиску новых знакомств.", key_search)
                        else:
                            bot.answer("😿 Упс! Ваш возраст должен быть в пределах от 14 до 100 лет!\n"
                                       "\n"
                                       "Если вы нечаянно ошиблись, то повторите попытку ввода:")
                    else:
                        bot.answer("🤚 Ваш возраст должен являться целым числом!\n"
                                   "\n"
                                   "Повторите попытку ввода возраста:")
                elif action[user_id] == "enter_sex":
                    sex = validate_sex(message)
                    if sex:
                        users[user_id][3] = sex
                        action[user_id] = "null"
                        bot.answer("🥳 Поздравляем! Вы успешно заполнили данные и теперь можете приступать к поиску новых знакомств.", key_search)
                    else:
                        bot.answer("🤚 Вы указали недопустимый пол!\n"
                                   "\n"
                                   "Выберите свой пол на клавиатуре:", key_sex_choice)

                # Если пользователь заполнил все данные:
                elif action[user_id] == "null":
                    if message == "поиск!" or message == "поиск":
                        if user_id not in list(profiles.keys()):
                            bot.answer("🔎 Подбираем для вас наилучшие анкеты...")
                            try:
                                profiles[user_id] = search_users(users[user_id])
                                bot.answer("🥳 Анкеты успешно найдены!\n"
                                           "\n"
                                           "Используйте кнопку ниже, чтобы их просмотреть.", key_search)
                            except:
                                bot.answer("❌ Произошла ошибка при поиске анкет...", key_search)
                        if user_id not in list(offsets.keys()):
                            offsets[user_id] = 0
                        else:
                            profile_data = fetch_profiles(search_users(users[user_id]), user_id, offsets[user_id])
                            offsets[user_id] = profile_data[4]
                            bot.answer(f"💖 {profile_data[0]}, {profile_data[1]} лет\n"
                                       f"Ссылка на страницу: https://vk.com/id{profile_data[2]}", attachment=profile_data[3],
                                       keyboard=key_search)

except requests.ConnectionError or requests.ConnectTimeout:
    time.sleep(30)

except:
    traceback.print_exc()
