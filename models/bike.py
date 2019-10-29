from models.base import BaseModel

COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT + 1
    return COUNT


class Bike(BaseModel):
    def __init__(self, faker):
        super().__init__()
        self.id = increment()
        self.friendly_name = faker.first_name()
        self.current_location = None

    def __iter__(self):
        return iter([self.id, self.friendly_name])
