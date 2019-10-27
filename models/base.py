import uuid


class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()

    def __iter__(self):
        dictionary = self.__dict__
        if 'id' in dictionary:
            dictionary['id'] = int(dictionary['id'])
        return iter(dictionary.values())
