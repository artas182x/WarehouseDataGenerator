from generator import Generator
from config import Config
import csv
import os
from faker import Faker
import random


class Simulator:
    def __init__(self, config):
        self.faker = Faker("pl_PL")
        self.generator = Generator(config, self.faker)
        self.names = []
        self.surnames = []

        for i in range(10):
            self.names.append(self.faker.first_name())
            self.surnames.append(self.faker.last_name())

    def save_to_file(self, dir):
        with open(os.path.join(dir, 'klienci.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.clients:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'rowery.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.bikes:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'listastacji.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.stations:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'stanstacji.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.station_states:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'historiaserwisowania.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.service_history:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'historiawypozyczen.bulk'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.rental_history:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'historiapracy.csv'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            for cdr in self.generator.work_history:
                wr.writerow(cdr)

        with open(os.path.join(dir, 'historianaprawy.csv'), 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            for cdr in self.generator.repair_history:
                wr.writerow(cdr)

    def generate(self, start_date, end_date):
        self.generator.config.recalculate(start_date, end_date)
        self.generator.generate_bikes(self.generator.config.MAX_BIKES)
        self.generator.generate_stations()
        self.generator.generate_clients(self.generator.config.MAX_CLIENTS)
        self.generator.init_station_states()
        self.generator.generate_work_history(self.names, self.surnames)
        self.generator.simulation()

        self.save_to_file("T1-T2")

    def generate_next_date(self, start_date, end_date):
        self.generator.revaluate_station_states()
        self.generator.config.recalculate(start_date, end_date)

        self.generator.generate_work_history(self.names, self.surnames)
        self.generator.simulation()

        self.save_to_file("T2-T3")





# def simulate_day(self, day, is_workday):
#    for hour in range(24):
