import json

class KeyboardColor:
    PRIMARY = "primary"
    BLUE = PRIMARY
    SECONDARY = "secondary"
    WHITE = SECONDARY
    NEGATIVE = "negative"
    RED = NEGATIVE
    POSITIVE = "positive"
    GREEN = POSITIVE


class KeyboardGenerator:

    def __init__(self, one_time=True, inline=False):
        self.keyboard_json = dict()
        self.current_line = 0
        self.keyboard_json['one_time'] = one_time
        self.keyboard_json['buttons'] = []
        self.keyboard_json['inline'] = inline

    # Добавление текстовой кнопки:
    def add_text_button(self, text: str, payload: str = None, color: str = KeyboardColor.WHITE):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'text', 'label': text, 'payload': payload}, "color": color}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'text', 'label': text, 'payload': payload}, "color": color})

    # Добавление кнопки, которая откроет ссылку:
    def add_openlink_button(self, text: str, open_link: str, payload: str = None):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'open_link', 'label': text, 'link': open_link, 'payload': payload}}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'open_link', 'label': text, 'link': open_link, 'payload': payload}})

    # Добавление кнопки, которая запросит локацию у пользователя:
    def add_geolocation_button(self, payload: str = None):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'location', 'payload': payload}}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'location', 'payload': payload}})

    # Добавление кнопки, которая перенаправит на окно оплаты VK Pay:
    def add_open_vkpay_form_button(self, payment_hash: str, payload: str = None):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'vkpay', 'hash': payment_hash,'payload': payload}}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'vkpay', 'hash': payment_hash, 'payload': payload}})

    # Добавление кнопки, которая откроет VK Mini Apps:
    def add_open_miniapps_button(self, app_id: int, app_name: str, owner_id: int = None,  payload: str = None, navigation_hash: str = None):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'open_app', 'app_id': app_id, 'app_name': app_name, 'owner_id': owner_id, 'hash': navigation_hash, 'payload': payload}}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'open_app', 'app_id': app_id, 'app_name': app_name, 'owner_id': owner_id, 'hash': navigation_hash, 'payload': payload}})

    # Добавление Callback-кнопки:
    def add_callback_button(self, text: str, payload: str = None):
        if not self.keyboard_json['buttons']:
            self.keyboard_json['buttons'].append([{"action": {'type': 'callback', 'label': text, 'payload': payload}}])
        else:
            self.keyboard_json['buttons'][self.current_line].append({"action": {'type': 'callback', 'label': text, 'payload': payload}})

    def add_new_line(self):
        self.current_line += 1
        self.keyboard_json['buttons'].append([])

    def get_keyboard_json(self):
        return json.dumps(self.keyboard_json)
