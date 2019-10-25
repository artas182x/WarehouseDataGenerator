from enum import Enum
import datetime
from faker import Faker
import random


class Gender(Enum):
    K = 0
    M = 1


class Client:

    def __init__(self, id, faker):

        self.id = id
        self.gender = Gender.M if random.randint(0, 1) == 0 else Gender.K
        self.name = faker.first_name_male() if self.gender == Gender.M else faker.first_name_female()
        self.surname = faker.last_name_male() if self.gender == Gender.M  else faker.last_name_female()
        self.birthday = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)
