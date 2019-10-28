import random
from enum import Enum

from models.base import BaseModel

COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT+1
    return COUNT


class Gender(Enum):
    FEMALE = "k"
    MALE = "m"

    @classmethod
    def get_gender(cls):
        return random.choice([Gender.FEMALE, Gender.MALE])


class Client(BaseModel):
    def __init__(self, faker):

        self.faker = faker

        super().__init__()

        self.id = increment()

        self.gender = Gender.get_gender()
        self.name = self._generate_name()
        self.surname = self._generate_surname()
        self.birthday = self.faker.date_of_birth(
            tzinfo=None, minimum_age=18, maximum_age=100
        )

    def _generate_name(self):
        return (
            self.faker.first_name_male()
            if self.gender == Gender.MALE
            else self.faker.first_name_female()
        )

    def _generate_surname(self):
        return (
            self.faker.last_name_male()
            if self.gender == Gender.MALE
            else self.faker.last_name_female()
        )

    def __iter__(self):
        return iter([self.name, self.surname, self.gender.value, self.birthday, self.id])
