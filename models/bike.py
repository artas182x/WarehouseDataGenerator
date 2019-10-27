from models.base import BaseModel


class Bike(BaseModel):
    def __init__(self, faker):
        super().__init__()
        self.friendly_name = faker.first_name()
        self.current_location = None
