class Config:

    # TODO: Load from JSON or whatever

    def __init__(self, *, start_date, end_date):
        self.MAX_CLIENTS = 10000
        self.MAX_BIKES = 1000
        self.MAX_STATIONS = 30
        self.MAX_RENTAL_ENTRIES = 20000
        self.MAX_REPAIR_ENTRIES = 1000
        self.MAX_SERVICE_ENTRIES = 7000
        self.START_DATE = start_date

        self.DAYS = abs((end_date - start_date).days)
        self.STATION_STATES_ENTRIES = self.DAYS * 24
        self.RENTAL_ENTRIES_PER_DAY = int(self.MAX_RENTAL_ENTRIES/self.DAYS)
        self.REPAIR_ENTRIES_PER_DAY = int(self.MAX_REPAIR_ENTRIES/self.DAYS)
        self.SERVICE_ENTRIES_PER_DAY = int(self.MAX_REPAIR_ENTRIES/self.DAYS)
