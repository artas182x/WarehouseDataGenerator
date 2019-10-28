from models.base import BaseModel


class RentalHistory(BaseModel):
    def __init__(
        self, client_id, start_station_id, end_station_id, bike_id, start_date, end_date
    ):
        super().__init__()
        self.client_id = client_id
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id
        self.bike_id = bike_id
        self.start_date = start_date
        self.end_date = end_date
