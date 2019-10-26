from Generator import Generator
from Config import Config


class Simulator:
    def __init__(self, config):
        self.generator = Generator(config)

        self.generator.generate_bikes()
        self.generator.generate_stations()
        self.generator.generate_clients()
        self.generator.init_bikes_location()
        self.generator.init_station_states()

   # def simulate_day(self, day, is_workday):
    #    for hour in range(24):



