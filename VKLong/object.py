class message_new:
    def __init__(self, response):
        self.response = response
        self.message_object = response['message']
        self.message_date = self.message_object['date']
        self.from_id = self.message_object['from_id']
        self.message_id = self.message_object['id']
        self.out = self.message_object['out']
        self.conversation_message_id = self.message_object['conversation_message_id']
        self.forward_messages = self.message_object['fwd_messages']
        self.is_important = self.message_object['important']
        self.is_hidden = self.message_object['is_hidden']
        self.random_id = self.message_object['random_id']
        self.text = self.message_object['text']
        self.client_info = response['client_info']
        self.button_actions = self.client_info['button_actions']
