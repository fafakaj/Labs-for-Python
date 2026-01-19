class Currency:
    def __init__(self, num_code: str, char_code: str, name: str,
                 value: float = 0.0, nominal: int = 1, id: int = None):
        self.__id = id
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def id(self):
        return self.__id

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, val: str):
        if not val or len(val) != 3:
            raise ValueError("Числовой код валюты должен состоять из 3 символов")
        self.__num_code = val

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str):
        if not val or len(val) != 3:
            raise ValueError("Буквенный код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val: str):
        if not val:
            raise ValueError("Название валюты не может быть пустым")
        self.__name = val

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: float):
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = val

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, val: int):
        if val <= 0:
            raise ValueError("Номинал должен быть положительным числом")
        self.__nominal = val

    def to_dict(self):
        """Преобразование объекта в словарь для БД"""
        return {
            'id': self.__id,
            'num_code': self.__num_code,
            'char_code': self.__char_code,
            'name': self.__name,
            'value': self.__value,
            'nominal': self.__nominal
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря (например, из БД)"""
        return cls(
            id=data.get('id'),
            num_code=data.get('num_code'),
            char_code=data.get('char_code'),
            name=data.get('name'),
            value=data.get('value'),
            nominal=data.get('nominal')
        )

    def __repr__(self):
        return f"Currency({self.char_code}: {self.value})"