from enum import Enum
from models.base import BaseModel
import random


class State(Enum):
    REPAIR = "repair"
    REPAIRED = "repaired"
    WONT_REPAIR = "wont_repair"


def _get_random_workshop_name():
    return "Serwis rowerowy #" + random.randint(1, 10).__str__()


class RepairHistory(BaseModel):

    def __init__(self, id, bike_id, workshop_name, state: State, date):
        super().__init__()
        self.id = id
        self.workshop_name = workshop_name
        self.date = date
        self.state = state
        self.bike_id = bike_id
