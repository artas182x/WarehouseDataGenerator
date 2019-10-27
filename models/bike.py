from models.base import BaseModel
import uuid


class Bike():
    def __init__(self, faker):
        self.id = uuid.uuid4()
        self.friendly_name = faker.first_name()
        self.current_location = 0
