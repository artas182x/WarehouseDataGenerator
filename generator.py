from models.client import Client
from models.bike import Bike
from models.station import Station
from models.station_state import StationState
from models.work_history import WorkHistory
from models.rental_history import RentalHistory
from models.service_history import ServiceHistory
from datetime import timedelta
from faker import Faker
import random


# TODO change to use python daterange
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
        self.rental_history = []
        self.service_history = []

    def simulation(self):
        print("Simulating business process")
        self.simulate_hour(False, self.config.START_DATE, 30, 3, 3)

    def simulate_hour(self, is_workday, date, rental_number, service_number, broken_bikes_number):

        # We will clone station states to new hour so we can update it during simulation
        previous_hour_states = [
            x
            for x in self.station_states
            if x.date == self.station_states[-1].date
        ]
        for x in previous_hour_states:
            x.date = x.date + timedelta(hours=1)

        self.station_states.extend(previous_hour_states)

        # We will use local history entries and commit them to global database to avoid logical conflicts
        local_history_entries = []
        local_service_history = []

        for i in range(rental_number):

            starting_stations = [
                x
                for x in self.station_states
                if x.date == self.station_states[-1].date and x.free_bikes > 0
            ]

            start_station = random.choice(starting_stations)
            end_station = random.choice(self.stations)

            bike = random.choice([
                x
                for x in self.bikes
                if x.current_location == start_station.station_id
            ])

            client = random.choice(self.clients)

            # Start renting
            start_station.free_bikes -= 1
            bike.current_location = 0
            rental_start_date = date + timedelta(minutes=random.randint(0, 30))
            rental_end_date = rental_start_date + timedelta(minutes=random.randint(5, 29))

            rental_history_entry = RentalHistory(client.id, start_station.id, end_station.id, bike.id,
                                                 rental_start_date, rental_end_date)

            local_history_entries.append(rental_history_entry)

        for i in range(service_number):

            # Choose station with the most number of bikes
            most_frequent_station = sorted([
                x
                for x in self.station_states
                if x.date == self.station_states[-1].date and x.free_bikes > 0
            ], key=lambda z: z.free_bikes, reverse=True)[0]

            bike = random.choice([
                x
                for x in self.bikes
                if x.current_location == most_frequent_station.station_id
            ])

            most_frequent_station.free_bikes -= 1
            bike.current_location = 0

            least_frequent_station = sorted([
                x
                for x in self.station_states
                if x.date == self.station_states[-1].date and x.free_bikes > 0
            ], key=lambda z: z.free_bikes)[0]

            local_service_history.append(ServiceHistory(most_frequent_station.station_id,
                                                        least_frequent_station.station_id,
                                                        date + timedelta(minutes=random.randint(0, 59)), bike.id))

        # Updating station states after all operations
        for i in range(rental_number):

            for entry in local_history_entries:
                station_state = [
                    x
                    for x in self.station_states
                    if x.date == self.station_states[-1].date and x.station_id == entry.end_station_id
                ][0]
                bike = [
                    x
                    for x in self.bikes
                    if x.id == entry.bike_id
                ][0]

                station_state.free_bikes += 1
                bike.current_location = entry.end_station_id

            for entry in local_service_history:
                station_state = [
                    x
                    for x in self.station_states
                    if x.date == self.station_states[-1].date and x.station_id == entry.end_station_id
                ][0]
                bike = [
                    x
                    for x in self.bikes
                    if x.id == entry.bike_id
                ][0]

                station_state.free_bikes += 1
                bike.current_location = entry.end_station_id

        self.service_history.extend(local_service_history)
        self.rental_history.extend(local_history_entries)


    def generate_clients(self):
        print("Generating clients")
        self.clients = [Client(self.faker) for _ in range(self.config.MAX_CLIENTS)]

    def generate_bikes(self):
        print("Generating bikes")
        self.bikes = [Bike(self.faker) for _ in range(self.config.MAX_BIKES)]

    def generate_stations(self, offset=0):
        print("Generating stations")
        avg_capacity = self.config.MAX_BIKES / self.config.MAX_STATIONS
        min_capacity = int(0.7 * avg_capacity)
        max_capacity = int(1.3 * avg_capacity)

        self.stations = [
            Station(capacity=random.randint(min_capacity, max_capacity), radius=0.85, faker=self.faker)
            for _ in range(self.config.MAX_STATIONS)
        ]

        # Some rarely visited stations
        for i in range(1, 5):
            self.stations[
                random.randint(0, self.config.MAX_STATIONS - 1)
            ].rarely_visited = True

        # Mark some stations as workplaces
        for i in range(1, int(self.config.MAX_STATIONS * 0.2)):
            index = random.randint(0, self.config.MAX_STATIONS - 1)
            self.stations[index].workplace = True

            # And some of them will be overloaded
            self.stations[index].overloaded = (
                True if random.randint(1, 10) < 3 else False
            )

    def generate_work_history(self):
        print("Generating work history")
        workers = 10

        names = []
        surnames = []

        for i in range(workers):
            names.append(self.faker.first_name())
            surnames.append(self.faker.last_name())

        for index, single_date in enumerate(
            datarange(self.config.START_DATE, self.config.END_DATE, diff=7)
        ):
            rand_index = random.randrange(workers)
            self.work_history.append(
                WorkHistory(
                    id=index,
                    name=names[rand_index],
                    surname=surnames[rand_index],
                    work_start_date=single_date,
                    work_finish_date=single_date + timedelta(hours=7),
                )
            )

    def init_station_states(self):
        print("Initializing stations states")
        # Generate empty first station states
        self.station_states = [
            StationState(
                date=self.config.START_DATE, station_id=station.id, free_bikes=0
            )
            for station in self.stations
        ]

        for i in range(self.config.MAX_BIKES):
            curr_station = random.choice(self.stations)
            self.bikes[i].current_location = curr_station.id
            el = [
                x
                for x in self.station_states
                if x.date == self.config.START_DATE and x.station_id == curr_station.id
            ][0]

            el.free_bikes += 1


# TODO repair history, service history
