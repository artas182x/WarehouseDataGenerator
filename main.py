from tables.Client import Client
from tables.Bike import Bike
from tables.Station import Station
from faker import Faker

if __name__ == "__main__":
    faker = Faker("pl_PL")
    bike = Bike(1, faker)
    station = Station(1, faker, capacity=20, radius=0.0001)
    client = Client(1, faker)
    pass
