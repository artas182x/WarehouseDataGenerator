import random
import copy
import math
from datetime import timedelta

from faker import Faker

from models.bike import Bike
from models.client import Client
from models.rental_history import RentalHistory
from models.service_history import ServiceHistory
from models.station import Station
from models.station_state import StationState
from models.work_history import WorkHistory
from models.repair_history import RepairHistory
from models.repair_history import State
from models.repair_history import _get_random_workshop_name


# TODO change to use python daterange
# diff - specifies hours loop should skip. Diff 24 means that loop will iterate every each day
def datarange(start_date, end_date, diff=24):
    for n in range(int((end_date - start_date).days * 24 - diff)):
        yield start_date + timedelta(hours=n + diff)


class Generator:
    def __init__(self, config, faker):
        self.config = config
        self.faker = faker

        self.clients = []
        self.bikes = []
        self.stations = []
        self.station_states = []
        self.work_history = []
        self.rental_history = []
        self.service_history = []
        self.repair_history = []

        self.last_repair_history_index = 1

    def simulation(self):
        print("Simulating business process")

        weekend_days = self._get_number_of_weekend_days()
        days = (self.config.END_DATE-self.config.START_DATE).days
        work_days = days-weekend_days

        print("Will be additional " + (days*24*self.config.MAX_BIKES).__str__() + " records")

        for i in datarange(self.config.START_DATE, self.config.END_DATE, diff=1):
            is_weekday = i.weekday() < 5
            print("Simulating: " + i.__str__())
            self.simulate_hour(is_weekday, start_date=i, number_of_rented_bikes=math.ceil(self.config.RENTAL_ENTRIES_PER_DAY/24),
                               number_of_bikes_broken=math.ceil(self.config.REPAIR_ENTRIES_PER_DAY/48),
                               number_of_bikes_serviced=math.ceil(self.config.SERVICE_ENTRIES_PER_DAY))

            if i != self.config.END_DATE:
                # We will clone station states to new hour so we can update it during simulation
                previous_hour_states = copy.deepcopy(self._get_previous_hour_states())
                for x in previous_hour_states:
                    x.date = x.date + timedelta(hours=1)
                    x.id = x.id + self.config.MAX_STATIONS
                self.station_states.extend(previous_hour_states)

    def revaluate_station_states(self):
        previous_hour_states = copy.deepcopy(self._get_previous_hour_states())
        for x in previous_hour_states:
            x.date = x.date + timedelta(hours=1)
            x.id = x.id + self.config.MAX_STATIONS

        stations = self._get_stations(False)

        for x in stations:
            try:
                station_state = self._get_last_station_state_by_station_id(x.id)
            except:
                station_state = StationState(previous_hour_states[1].date, x.id, 0)
                station_state.id = previous_hour_states[-1].id + 1
                previous_hour_states.append(station_state)


        self.station_states.extend(previous_hour_states)


    def _get_number_of_weekend_days(self):
        number = 0
        for i in datarange(self.config.START_DATE, self.config.END_DATE, diff=24):
            if i.weekday() >= 5:
                number += 1

        return number

    def _get_latest_hour(self):
        return self.station_states[-1].date

    def _get_previous_hour_states(self):
        latest_hour = self._get_latest_hour()
        return [x for x in self.station_states if x.date == latest_hour]

    def _get_starting_stations_states(self, filter_unused):
        if filter_unused:
            used_stations = [x for x in self.stations if not x.became_not_used]

            return [
                x
                for x in self.station_states[-1 * self.config.MAX_STATIONS:]
                if x.date == self._get_latest_hour() and x.free_bikes > 0 and self._station_exist_in_list(x.station_id,
                                                                                                          used_stations)
            ]
        else:

            return [
                x
                for x in self.station_states[-1 * self.config.MAX_STATIONS:]
                if x.date == self._get_latest_hour() and x.free_bikes > 0
            ]

    def _get_stations(self, filter_unused):
        if filter_unused:
            return [x for x in self.stations if not x.became_not_used]
        else:
            return self.stations

    def _get_bikes_at_station(self, station_id):
        return [x for x in self.bikes if x.current_location == station_id]

    def _get_last_station_state_by_station_id(self, station_id):
        return [x for x in self.station_states[-1 * self.config.MAX_STATIONS:] if x.station_id == station_id and x.date == self._get_latest_hour()][0]

    def _get_not_used_bikes(self):
        return [x for x in self.bikes if x.current_location is not None]

    def _generate_bike_repair_finish_state(self, probability_of_total_damage):
        number = random.randint(0,10)
        return State.WONT_REPAIR if 0.1*number < probability_of_total_damage \
            else State.REPAIRED

    def simulate_hour(
            self,
            is_workday,
            start_date,
            number_of_rented_bikes,
            number_of_bikes_serviced,
            number_of_bikes_broken,
    ):
        # We will use local history entries and commit them to global database to avoid logical conflicts
        local_rental_histories = []
        local_service_histories = []
        local_repair_history = []

        for _ in range(number_of_rented_bikes):
            # this needs to be refreshed because station can have 0 free bikes
            starting_stations_states = self._get_starting_stations_states(filter_unused=self.config.STATIONS_THAT_BECAME_NOT_USED)
            start_station_state = random.choice(starting_stations_states)
            end_station = random.choice(self._get_stations(filter_unused=self.config.STATIONS_THAT_BECAME_NOT_USED))
            bike = random.choice(
                self._get_bikes_at_station(start_station_state.station_id)
            )
            client = random.choice(self.clients)

            # Start renting
            start_station_state.free_bikes -= 1
            bike.current_location = None
            rental_start_date = start_date + timedelta(minutes=random.randint(0, 30))
            rental_end_date = rental_start_date + timedelta(
                minutes=random.randint(5, 29)
            )
            rental_history_entry = RentalHistory(
                client.id,
                start_station_state.station_id,
                end_station.id,
                bike.id,
                rental_start_date,
                rental_end_date,
            )
            local_rental_histories.append(rental_history_entry)

        for _ in range(number_of_bikes_serviced):
            # Choose station with the most number of bikes
            most_frequent_station = self._get_used_by_employees_station_states(reverse=True)[0]
            bike = random.choice(
                self._get_bikes_at_station(most_frequent_station.station_id)
            )
            most_frequent_station.free_bikes -= 1
            bike.current_location = None
            least_frequent_station = self._get_used_by_employees_station_states(reverse=False)[0]
            local_service_histories.append(
                ServiceHistory(
                    most_frequent_station.station_id,
                    least_frequent_station.station_id,
                    start_date + timedelta(minutes=random.randint(0, 59)),
                    bike.id,
                )
            )

        for _ in range(number_of_bikes_broken):
            bike = random.choice(self._get_not_used_bikes())
            station_state = self._get_last_station_state_by_station_id(bike.current_location)

            station_state.free_bikes -= 1
            bike.current_location = None

            workshop_name = _get_random_workshop_name()

            repair_history_entry = RepairHistory(self.last_repair_history_index, bike.id, workshop_name, State.REPAIR,
                                                 start_date + timedelta(minutes=random.randint(0, 5)))

            self.last_repair_history_index += 1

            repair_finish_state = self._generate_bike_repair_finish_state(probability_of_total_damage=0.05)

            repair_history_entry_finish = RepairHistory(self.last_repair_history_index, bike.id, workshop_name,
                                                        repair_finish_state, repair_history_entry.date +
                                                        timedelta(minutes=random.randint(40, self.config.BIKE_REPAIR_TIME)))

            self.last_repair_history_index += 1

            local_repair_history.append(repair_history_entry)
            local_repair_history.append(repair_history_entry_finish)


        # Updating station states after all operations
        for rental in local_rental_histories:
            station_state = [
                x
                for x in self.station_states[-1 * self.config.MAX_STATIONS:]
                if x.date == self._get_latest_hour()
                    and x.station_id == rental.end_station_id
            ][0]
            bike = [x for x in self.bikes if x.id == rental.bike_id][0]
            station_state.free_bikes += 1
            bike.current_location = rental.end_station_id

        for rental in local_service_histories:
            station_state = [
                x
                for x in self.station_states[-1 * self.config.MAX_STATIONS:]
                if x.date == self._get_latest_hour()
                    and x.station_id == rental.end_station_id
            ][0]
            bike = [x for x in self.bikes if x.id == rental.bike_id][0]
            station_state.free_bikes += 1
            bike.current_location = rental.end_station_id

        for repair in local_repair_history:
            bikes_repaired = [x for x in self.bikes if x.id == repair.bike_id and repair.state == State.REPAIRED]

            if bikes_repaired.__len__() > 0:
                curr_station = random.choice(self.stations)
                bikes_repaired[0].current_location = curr_station.id
                for station_state in self.station_states:
                    if (
                            station_state.date == self._get_latest_hour()
                            and station_state.station_id == curr_station.id
                    ):
                        station_state.free_bikes += 1
                        break

        self.service_history.extend(local_service_histories)
        self.rental_history.extend(local_rental_histories)
        self.repair_history.extend(local_repair_history)

    def _get_used_by_employees_station_states(self, reverse):
        used_stations = [x for x in self.stations if not x.rarely_visited]

        return sorted(
            [x for x in self.station_states[-1 * self.config.MAX_STATIONS:] if x.date == self._get_latest_hour() and
             self._station_exist_in_list(x.station_id, used_stations)],
            key=lambda z: z.free_bikes,
            reverse=reverse,
        )

    def _station_exist_in_list(self, id, list):
        for x in list:
            if x.id == id:
                return True

        return False

    def _get_sorted_stations(self, reverse):
        return sorted(
            [x for x in self.station_states[-1 * self.config.MAX_STATIONS:] if x.date == self._get_latest_hour()],
            key=lambda z: z.free_bikes,
            reverse=reverse,
        )

    def generate_clients(self, number):
        print("Generating clients")
        for i in range(number):
            self.clients.append(Client(self.faker))

    def generate_bikes(self, number):
        print("Generating bikes")
        for i in range(number):
            self.bikes.append(Bike(self.faker))

    def mark_some_stations_as_rarely_visited(self):
        # Some rarely visited stations
        for i in range(1, 5):
            self.stations[
                random.randint(0, self.config.MAX_STATIONS - 1)
            ].rarely_visited = True

    def mark_some_stations_as_not_used(self):
        # Some not used in T2 stations
        for i in range(1, 5):
            self.stations[
                random.randint(0, self.config.MAX_STATIONS - 1)
            ].became_not_used = True

    def add_stations(self, min_capacity, max_capacity, number):
        for i in range (number):
            self.stations.append(
                Station(
                    capacity=random.randint(min_capacity, max_capacity),
                    radius=0.85,
                    faker=self.faker,
                ))

    def generate_stations(self, offset=0):
        print("Generating stations")
        avg_capacity = self.config.MAX_BIKES / self.config.MAX_STATIONS
        min_capacity = int(0.7 * avg_capacity)
        max_capacity = int(1.3 * avg_capacity)

        self.add_stations(min_capacity, max_capacity, self.config.MAX_STATIONS)
        self.mark_some_stations_as_rarely_visited()
        self.mark_some_stations_as_not_used()

        # Mark some stations as workplaces
        for i in range(1, int(self.config.MAX_STATIONS * 0.2)):
            index = random.randint(0, self.config.MAX_STATIONS - 1)
            self.stations[index].workplace = True

            # And some of them will be overloaded
            self.stations[index].overloaded = (
                True if random.randint(1, 10) < 3 else False
            )

    def generate_work_history(self, names, surnames):
        print("Generating work history")

        for index, single_date in enumerate(
            datarange(self.config.START_DATE, self.config.END_DATE, diff=7)
        ):
            rand_index = random.randrange(len(names))
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
            for station_state in self.station_states:
                if (
                        station_state.date == self.config.START_DATE
                        and station_state.station_id == curr_station.id
                ):
                    station_state.free_bikes += 1
                    break


# TODO repair history, service history
