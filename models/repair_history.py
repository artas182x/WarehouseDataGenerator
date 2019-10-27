from enum import Enum

from models.base import BaseModel


class State(Enum):
    REPAIR = "repair"
    REPAIRED = "repaired"
    WONT_REPAIR = "wont_repair"


class RepairHistory(BaseModel):
    def __init__(self, id, bike_id, state: State, date, workshop_name):
        super().__init__()
        self.id = id
        self.workshop_name = workshop_name
        self.date = date
        self.state = state
        self.bike_id = bike_id
