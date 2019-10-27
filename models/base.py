import uuid


class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
