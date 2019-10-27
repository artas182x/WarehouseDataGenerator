from models.base import BaseModel


class Station(BaseModel):
    def __init__(
            self,
            capacity,
            radius,
            faker,
            rarely_visited=False,
            overloaded=False,
            workplace=False,
    ):
        super().__init__()
        self.faker = faker
        self.name = self.faker.street_address()
        self.capacity = capacity
        self.latitude = self.faker.coordinate(center=54.324846, radius=radius)
        self.longitude = self.faker.coordinate(center=18.636886, radius=radius)

        # FLAGS
        self.rarely_visited = rarely_visited
        self.overloaded = overloaded
        self.workplace = workplace
