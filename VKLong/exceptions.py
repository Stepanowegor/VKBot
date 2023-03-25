class VKLongBotExceptions (Exception):
    # Ошибки использования API:
    class API (Exception):
        class WrongArgumentsType (Exception):
            def __init__(self, error_text):
                pass