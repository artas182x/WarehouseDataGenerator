from models.base import BaseModel


class ServiceHistory(BaseModel):
    def __init__(self, start_station_id, end_station_id, date, bike_id):
        super().__init__()
        self.date = date
        self.end_station_id = end_station_id
        self.start_station_id = start_station_id
        self.bike_id = bike_id
