class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: str):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID подписки должен быть положительным целым числом")
        self._id = value

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
        self._user_id = value

    @property
    def currency_id(self) -> str:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID валюты должен быть непустой строкой")
        self._currency_id = value.strip()