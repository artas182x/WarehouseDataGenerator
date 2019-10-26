class Bike:

    def __init__(self, id, faker):

        self.id = id
        self.friendlyname = faker.first_name()

        self.current_location = 0
