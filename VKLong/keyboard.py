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

    def get_keyboard_json(self):
        return json.dumps(self.keyboard_json)
