import uuid

from faker import Faker


class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
        self.faker = Faker("pl_PL")
