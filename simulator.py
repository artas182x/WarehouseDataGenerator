from generator import Generator
from config import Config
import csv


class Simulator:
    def __init__(self, config):
        self.generator = Generator(config)

        self.generator.generate_bikes()
        self.generator.generate_stations()
        self.generator.generate_clients()
        self.generator.init_station_states()
        self.generator.generate_work_history()
        self.generator.simulation()

    def save_to_file(self):
        with open('klienci.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.clients:
                wr.writerow(cdr)

        with open('rowery.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.bikes:
                wr.writerow(cdr)

        with open('listastacji.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.stations:
                wr.writerow(cdr)

        with open('stanstacji.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.station_states:
                wr.writerow(cdr)

        with open('historiaserwisowania.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.service_history:
                wr.writerow(cdr)

        with open('historiawypozyczen.bulk', 'w', newline='\n') as csv_file:
            wr = csv.writer(csv_file, delimiter='|')
            for cdr in self.generator.rental_history:
                wr.writerow(cdr)

# def simulate_day(self, day, is_workday):
#    for hour in range(24):
