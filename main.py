from datetime import date

from config import Config
from simulator import Simulator

# TODO What we need:
# At least one station which became not used from T2 to T3 comparing to T1 to T2 time.
# Some stations should be overloaded
# Bike repair times should be different in T1 and T2 DONE: BIKE_REPAIR_TIME
# Broken bikes number should be different in T1 and T2 DONE: MAX_REPAIR_ENTRIES
# Some stations should be more used between 8:00-10.00 AM and some between 4.00-6.00 PM
# At night all stations should have at least one bike
# At weekends people should not rent bikes from workplaces
# On work days between 12:00-14:00 station where are workplaces should be overloaded
# On time T2-T3 we should add some stations (requirement from instruction)
# On time T2-T3 we should add some bikes (requirement from instruction)
# At least one station should be rarely visited by employee DONE

if __name__ == "__main__":
    T1 = date(2017, 12, 5)
    T2 = date(2018, 11, 5)
    T3 = date(2019, 10, 15)

    config1 = Config(start_date=T1, end_date=T2)

    simulator1 = Simulator(config1)
    pass
