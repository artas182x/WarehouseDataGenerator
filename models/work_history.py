from models.base import BaseModel


class WorkHistory(BaseModel):
    def __init__(self, id, name, surname, work_start_date, work_finish_date):
        super().__init__()
        self.id = id
        self.name = name
        self.surname = surname
        self.work_start_date = work_start_date
        self.work_finish_date = work_finish_date
