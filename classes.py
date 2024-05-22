class TokenClass:
    """Класс для хранения информации, связанной с токеном."""
    def __init__(self, token: str, name: str = ''):
        self.token: str = token  # Токен.
        self.name: str = name  # Название токена.
