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

    def generate_clients(self, starting_index=1):
        for i in range(starting_index, self.config.MAX_CLIENTS):
            self.clients.append(Client(i, self.faker))

    def generate_bikes(self, starting_index=1):
        for i in range(starting_index, self.config.MAX_BIKES):
            self.bikes.append(Bike(i, self.faker))

    def generate_stations(self, starting_index=1):
        avg_capacity = self.config.MAX_BIKES/self.config.MAX_STATIONS
        min_capacity = int(0.7*avg_capacity)
        max_capacity = int(1.3*avg_capacity)

        for i in range(starting_index, self.config.MAX_BIKES):
            self.stations.append(Station(i, self.faker, capacity=random.randint(min_capacity, max_capacity),
                                         radius=0.85))

        pass
