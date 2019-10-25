from enum import Enum
import datetime
from faker import Faker
import random


class Plec(Enum):
    K = 0
    M = 1


class Klienci:

    def __init__(self, id, faker):

        self.id = id
        self.plec = Plec.M if random.randint(0, 1) == 0 else Plec.K
        self.imie = faker.first_name_male() if self.plec == Plec.M else faker.first_name_female()
        self.nazwisko = faker.last_name_male() if self.plec == Plec.M  else faker.last_name_female()
        self.data_urodzenia = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)
