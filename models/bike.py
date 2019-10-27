from models.base import BaseModel


class Bike(BaseModel):
    def __init__(self):
        super().__init__()
        self.friendly_name = self.faker.first_name()
        self.current_location = 0
