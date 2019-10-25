class Station:

    def __init__(self, id, faker, *, capacity, radius):

        self.id = id
        self.name = faker.street_address()
        self.capacity = capacity
        self.latitude = faker.coordinate(center=54.324846, radius=radius)
        self.longitude = faker.coordinate(center=18.636886, radius=radius)
