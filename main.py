from tables.Klienci import Klienci
from faker import Faker

if __name__ == "__main__":
    faker = Faker("pl_PL")
    print(Klienci(1, faker, "1920-02-20", "1930-03-20").imie)
