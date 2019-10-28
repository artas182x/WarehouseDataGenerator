import uuid

COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT+1
    return COUNT


class BaseModel:
    def __init__(self):
        self.id = increment()

    def __iter__(self):
        dictionary = self.__dict__
        if 'id' in dictionary:
            dictionary['id'] = int(dictionary['id'])
        return iter(dictionary.values())
