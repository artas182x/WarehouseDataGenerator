from datetime import datetime
import math


class Config:

    # TODO: Load from JSON or whatever

    def __init__(self, *, start_date, end_date):
        self.MAX_CLIENTS = 1000
        self.MAX_BIKES = 1000
        self.MAX_STATIONS = 30
        self.MAX_RENTAL_ENTRIES = 1000
        self.MAX_REPAIR_ENTRIES = 50
        self.MAX_SERVICE_ENTRIES = 500
        self.MAX_WORK_HISTORY_ENTRIES = 2000

        self.BIKE_REPAIR_TIME = 55
        self.STATIONS_THAT_BECAME_NOT_USED = False

        self.START_DATE = None
        self.END_DATE = None
        self.DAYS = None
        self.STATION_STATES_ENTRIES = None
        self.RENTAL_ENTRIES_PER_DAY = None
        self.REPAIR_ENTRIES_PER_DAY = None
        self.SERVICE_ENTRIES_PER_DAY = None

        self.recalculate(start_date, end_date)

    def recalculate(self, start_date, end_date):
        self.START_DATE = datetime.combine(start_date, datetime.min.time())
        self.END_DATE = datetime.combine(end_date, datetime.min.time())
        self.DAYS = abs((end_date - start_date).days)
        self.STATION_STATES_ENTRIES = self.DAYS * 24
        self.RENTAL_ENTRIES_PER_DAY = math.ceil(self.MAX_RENTAL_ENTRIES / self.DAYS)
        self.REPAIR_ENTRIES_PER_DAY = math.ceil(self.MAX_REPAIR_ENTRIES / self.DAYS)
        self.SERVICE_ENTRIES_PER_DAY = math.ceil(self.MAX_REPAIR_ENTRIES / self.DAYS)
