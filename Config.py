class Config:

    # TODO: Load from JSON or whatever

    def __init__(self, *, start_date, end_date):
        self.MAX_CLIENTS = 10000
        self.MAX_BIKES = 1000
        self.MAX_STATIONS = 30
        self.MAX_RENTAL_ENTRIES = 20000
        self.MAX_REPAIR_ENTRIES = 1000
        self.MAX_SERVICE_ENTRIES = 7000
        self.MAX_STATION_STATES_ENTRIES = abs((end_date - start_date).days) * 24
