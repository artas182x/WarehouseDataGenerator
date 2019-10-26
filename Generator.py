from Config import Config
from tables.Client import Client
from tables.Bike import Bike
from tables.Station import Station
from tables.StationState import StationState
from tables.WorkHistory import WorkHistory
from datetime import timedelta
from faker import Faker
import random


# diff - specifies hours loop should skip. Diff 24 means that loop will iterate every each day
def datarange(start_date, end_date, diff=24):
    for n in range(int((end_date - start_date).days * 24 - diff)):
        yield start_date + timedelta(hours=n + diff)


class Generator:

    def __init__(self, config):
        self.config = config
        self.faker = Faker("pl_PL")

        self.clients = []
        self.bikes = []
        self.stations = []
        self.station_states = []
        self.work_history = []

    def generate_clients(self, offset=0):
        print("Generating clients")
        for i in range(0, self.config.MAX_CLIENTS):
            self.clients.append(Client(i+offset, self.faker))

    def generate_bikes(self, offset=0):
        print("Generating bikes")
        for i in range(0, self.config.MAX_BIKES):
            self.bikes.append(Bike(i+offset, self.faker))

    def generate_stations(self, offset=0):
        print("Generating stations")
        avg_capacity = self.config.MAX_BIKES/self.config.MAX_STATIONS
        min_capacity = int(0.7*avg_capacity)
        max_capacity = int(1.3*avg_capacity)

        for i in range(0, self.config.MAX_STATIONS):
            self.stations.append(Station(i+offset, self.faker, capacity=random.randint(min_capacity, max_capacity),
                                         radius=0.85))

        # Some rarely visited stations
        for i in range(1, 5):
            self.stations[random.randint(0, self.config.MAX_STATIONS-1)].rarely_visited = True

        # Mark some stations as workplaces
        for i in range(1, int(self.config.MAX_STATIONS*0.2)):
            index = random.randint(0, self.config.MAX_STATIONS - 1)
            self.stations[index].workplaces = True

            # And some of them will be overloaded
            self.stations[index].overloaded = True if random.randint(1, 10) < 3 else False

    def generate_work_history(self):
        print("Generating work history")
        workers = 10

        names = []
        surnames = []

        for i in range(workers):
            names.append(self.faker.first_name())
            surnames.append(self.faker.last_name())

        for single_date in datarange(self.config.START_DATE, self.config.END_DATE, diff=7):
            rand_index = random.randint(0, workers-1)
            self.work_history.append(WorkHistory(names[rand_index], surnames[rand_index], single_date, single_date +
                                                 timedelta(hours=7)))

    def init_bikes_location(self):
        print("Initializing bikes")
        if self.stations.__sizeof__() == 0:
            raise ValueError("Stations list must be initialised first")

        for bike in self.bikes:
            bike.current_location = random.choice(self.stations).id

    def init_station_states(self):
        print("Initializing stations states")
        # Generate empty first station states
        for i in range(self.config.MAX_STATIONS):
            self.station_states.append(StationState(i, self.config.START_DATE, i, 0))

        for i in range(self.config.MAX_BIKES):
            curr_station = random.choice(self.stations)
            self.bikes[i].current_location = curr_station.id
            el = [x for x in self.station_states if x.date == self.config.START_DATE and
                  x.station_id == curr_station.id][0]












