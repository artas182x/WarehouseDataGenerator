from Config import Config
from tables.Client import Client
from tables.Bike import Bike
from tables.Station import Station
from faker import Faker
import random


class Generator:

    def __init__(self, config):
        self.config = config
        self.faker = Faker("pl_PL")

        self.clients = []
        self.bikes = []
        self.stations = []

    def generate_clients(self, offset=0):
        for i in range(1, self.config.MAX_CLIENTS):
            self.clients.append(Client(i+offset, self.faker))

    def generate_bikes(self, offset=0):
        for i in range(1, self.config.MAX_BIKES):
            self.bikes.append(Bike(i+offset, self.faker))

    def generate_stations(self, offset=0):
        avg_capacity = self.config.MAX_BIKES/self.config.MAX_STATIONS
        min_capacity = int(0.7*avg_capacity)
        max_capacity = int(1.3*avg_capacity)

        for i in range(1, self.config.MAX_BIKES):
            self.stations.append(Station(i+offset, self.faker, capacity=random.randint(min_capacity, max_capacity),
                                         radius=0.85))

        # Some rarely visited stations
        for i in range(1, 5):
            self.stations[random.randint(0, self.config.MAX_BIKES-1)].rarely_visited = True

        # Mark some stations as workplaces
        for i in range(1, self.config.MAX_STATIONS*0.2):
            index = random.randint(0, self.config.MAX_BIKES - 1)
            self.stations[index].workplaces = True

            # And some of them will be overloaded
            self.stations[index].overloaded = True if random.randint(1, 10) < 3 else False

    def init_bikes_location(self):
        if self.stations.__sizeof__() == 0:
            raise ValueError("Stations list must be initialised first")

        for bike in self.bikes:
            bike.current_location = random.choice(self.stations).id






