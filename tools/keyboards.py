from VKLong.keyboard import *

key_sex_choice = KeyboardGenerator()
key_sex_choice.add_text_button("Мужской", color=KeyboardColor.BLUE)
key_sex_choice.add_text_button("Женский", color=KeyboardColor.BLUE)
key_sex_choice = key_sex_choice.get_keyboard_json()

key_search = KeyboardGenerator()
key_search.add_text_button("Поиск!", color=KeyboardColor.BLUE)
key_search = key_search.get_keyboard_json()