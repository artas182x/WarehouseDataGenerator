from enum import Enum
from models.base import BaseModel
import random


COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT + 1
    return COUNT


class State(Enum):
    REPAIR = "W naprawie"
    REPAIRED = "Naprawiony"
    WONT_REPAIR = "Nie zostanie naprawiony"


def _get_random_workshop_name():
    return "Serwis rowerowy #" + random.randint(1, 10).__str__()


class RepairHistory(BaseModel):
    def __init__(self, id, bike_id, workshop_name, state: State, date, repair_id=-1):
        super().__init__()
        self.id = id
        self.workshop_name = workshop_name
        self.date = date
        self.state = state
        self.bike_id = bike_id
        self.repair_id = repair_id

        if self.repair_id == -1:
            self.repair_id = increment()

    def __iter__(self):
        return iter(
            [
                self.id,
                self.workshop_name,
                self.date,
                self.bike_id,
                self.state.value,
                self.repair_id,
            ]
        )
