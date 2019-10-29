from models.base import BaseModel

COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT + 1
    return COUNT


class ServiceHistory(BaseModel):
    def __init__(self, start_station_id, end_station_id, date, bike_id):
        super().__init__()
        self.id = increment()
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id
        self.date = date
        self.bike_id = bike_id
