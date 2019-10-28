import random
from datetime import date

from config import Config
from simulator import Simulator

# TODO What we need:
# At least one station which became not used from T2 to T3. DONE: STATIONS_THAT_BECAME_NOT_USED
# Some stations should be overloaded
# Bike repair times should be different in T1 and T2 DONE: BIKE_REPAIR_TIME
# Broken bikes number should be different in T1 and T2 DONE: MAX_REPAIR_ENTRIES
# Some stations should be more used between 8:00-10.00 AM and some between 4.00-6.00 PM
# At night all stations should have at least one bike
# At weekends people should not rent bikes from workplaces
# On work days between 12:00-14:00 station where are workplaces should be overloaded
# On time T2-T3 we should add some stations (requirement from instruction) DONE
# On time T2-T3 we should add some bikes (requirement from instruction) DONE
# At least one station should be rarely visited by employee DONE

config1 = None
simulator1 = None
T1 = date(2017, 12, 5)
T2 = date(2017, 12, 15)
T3 = date(2018, 2, 5)


def generate_t1_t2():
    global config1
    global simulator1

    config1 = Config(start_date=T1, end_date=T2)

    # T1-T2 Parameters
    config1.MAX_CLIENTS = 1000
    config1.MAX_BIKES = 1000
    config1.MAX_STATIONS = 30
    config1.MAX_RENTAL_ENTRIES = 10000
    config1.MAX_REPAIR_ENTRIES = 50
    config1.MAX_SERVICE_ENTRIES = 500
    config1.MAX_WORK_HISTORY_ENTRIES = 2000
    config1.BIKE_REPAIR_TIME = 55
    config1.STATIONS_THAT_BECAME_NOT_USED = False

    simulator1 = Simulator(config1)
    simulator1.generate(T1, T2)


def generate_t2_t3():
    global config1
    global simulator1

    # Adding some stations
    config1.MAX_STATIONS += 3
    simulator1.generator.add_stations(10, 20, number=3)

    # Adding some clients
    config1.MAX_CLIENTS += 3
    simulator1.generator.generate_clients(3)

    # Adding some bikes
    config1.MAX_BIKES += 3
    simulator1.generator.generate_bikes(3)

    # Change station capacity
    random.choice(simulator1.generator.stations).capacity = 5

    # T2-T3 Parameters
    config1.MAX_RENTAL_ENTRIES = 1000
    config1.MAX_REPAIR_ENTRIES = 50
    config1.MAX_SERVICE_ENTRIES = 500
    config1.MAX_WORK_HISTORY_ENTRIES = 2000

    config1.BIKE_REPAIR_TIME = 45
    config1.STATIONS_THAT_BECAME_NOT_USED = True

    simulator1.generate_next_date(T2, T3)


if __name__ == "__main__":

    generate_t1_t2()
    generate_t2_t3()
