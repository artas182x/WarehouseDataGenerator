from models.base import BaseModel


class StationState(BaseModel):
    def __init__(self, date, station_id, free_bikes):
        super().__init__()
        self.id = id
        self.date = date
        self.station_id = station_id
        self.free_bikes = free_bikes
