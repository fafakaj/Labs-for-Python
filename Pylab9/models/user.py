class User:
    def __init__(self, name: str, id: int = None):
        self.__id = id
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val: str):
        if not val:
            raise ValueError("Имя пользователя не может быть пустым")
        self.__name = val

    def to_dict(self):
        return {
            'id': self.__id,
            'name': self.__name
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name')
        )

    def __repr__(self):
        return f"User({self.id}: {self.name})"