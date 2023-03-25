import json
import random
import requests
from VKLong.object import *
from VKLong.exceptions import *


class Event:
    def __init__(self, update):
        self.type = update["updates"][0]['type']
        self.response = update['updates'][0]['object']
        if self.type == "message_new":
            self.object = message_new(self.response)
            if self.response['message']['peer_id'] < 2000000000:
                self.is_message_from_user = True
            else:
                self.is_message_from_user = False

class Bot:
    def __init__(self, token: str, api_version: int = 5.131, wait=25):
        self.token = token
        self.api_version = api_version
        self.wait = 25
        self.__api_link = "https://api.vk.com/method"
        self.__group_id = self.execute_api("groups.getById", {"access_token": token, 'v': api_version})[0]['id']
        self.__last_update = None

    # Функция вызова API:
    def execute_api(self, method, parameters):
        if type(parameters) != dict:
            raise VKLongBotExceptions.API.WrongArgumentsType("Parameters type for execute API-request needed be a dictionary!")
        else:
            parameters['access_token'] = self.token
            parameters['v'] = self.api_version
            response = requests.get(f"{self.__api_link}/{method}", params=parameters).json()
            return response['response']

    # Получение данных сервера:
    def get_actual_server_data(self):
        response = self.execute_api("groups.getLongPollServer", {"group_id": self.__group_id})
        return {"server": response['server'], "key": response['key'], "ts": response['ts']}

    # Получение обновлений:
    def get_updates(self, function):
        server_data = self.get_actual_server_data()
        server = server_data['server']
        server_ts = int(server_data['ts'])
        server_key = server_data['key']
        while True:
            response = requests.get(f"{server}?act=a_check&key={server_key}&ts={server_ts}&wait={self.wait}").json()
            try:
                error_number = int(response['failed'])
                match error_number:
                    case 1:
                        server_ts = response['ts']
                    case 2:
                        server_key = self.get_actual_server_data()['key']
                    case 3:
                        server = self.get_actual_server_data()
                        server_ts = server['ts']
                        server_key = server['key']
            except KeyError:
                try:
                    self.__last_update = response
                    function(Event(response))
                except IndexError:
                    pass
                server_ts += 1

    # Отправка сообщений:
    def send_message(self, peer_id: int or list, message: str = None, keyboard = None, attachment: str = None, random_id: int = 0,
                     reply_id: int = None, forward_messages = None, sticker_id: int = None, payload = None, dont_parse_links: int = None, disable_mentions: int = None):
        return self.execute_api("messages.send",
                         {"peer_id": peer_id, "message": message, "keyboard": keyboard, "attachment": attachment, "random_id": random_id,
                          "reply_id": reply_id, "forward_messages": forward_messages, "sticker_id": sticker_id,
                          "payload": payload, "dont_parse_links": dont_parse_links, "disable_mentions": disable_mentions})

    # Ответ на сообщение (без указания peer_id, сообщение будет отправлено последнему отправителю):

    def answer(self, message: str = None, keyboard = None, attachment: str = None, random_id: int = 0,
                     reply_id: int = None, forward_messages = None, sticker_id: int = None, payload = None, dont_parse_links: int = None, disable_mentions: int = None):
        peer_id = self.__last_update['updates'][0]['object']['message']['peer_id']
        return self.execute_api("messages.send",
                         {"peer_id": peer_id, "message": message, "keyboard": keyboard, "attachment": attachment, "random_id": random_id,
                          "reply_id": reply_id, "forward_messages": forward_messages, "sticker_id": sticker_id,
                          "payload": payload, "dont_parse_links": dont_parse_links, "disable_mentions": disable_mentions})

    # Подробнее: https://dev.vk.com/api/bots/development/keyboard
    def send_message_event_answer(self, event_id: str, user_id: int, peer_id: int, event_data: dict):
        self.execute_api("messages.sendMessageEventAnswer", {'event_id': event_id, 'user_id': user_id, 'peer_id': peer_id, 'event_data': json.dumps(event_data)})
