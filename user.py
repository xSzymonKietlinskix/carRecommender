import csv
import pandas as pd


class DecodedUser:
    def __init__(self,  economy, comfort, driving_style, purpose, min_price, max_price, id_usr=0, purpose_str=""):
        self.purpose_str = purpose_str
        self.max_price = float(max_price)
        self.min_price = float(min_price)
        self.id_usr = id_usr
        self.purpose = purpose
        self.driving_style = driving_style
        self.comfort = comfort
        self.economy = economy


    def save_user_rating(self, car_id, rating):
        with open('users_ratings.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            row = str(self.id_usr) + ';' + str(car_id) + ';' + str(rating)
            writer.writerow([row])

    def values(self):
        return self.purpose_str, self.economy, self.comfort, self.min_price, self.max_price


class User:
    def __init__(self, przeznaczenie, ekonomia, wygoda, styl_jazdy, min_price, max_price):
        self.max_price = max_price
        self.min_price = min_price
        self.styl_jazdy = styl_jazdy
        self.wygoda = wygoda
        self.ekonomia = ekonomia
        self.przeznaczenie = przeznaczenie


    def decode(self):
        przeznaczenie_dict = {
            'Rodzinny': ['D', 'E', 'K'],
            'Miejski': ['A', 'B', 'C'],
            'Uniwersalny': ['C', 'D', 'E'],
            'Trasy': ['D', 'E', 'F', 'K'],
            'Sportowy': ['G'],
        }
        styl_jazdy_dict = {
            'defensywny': -1,
            'agresywny': 1,
            'neutralny': 0,
        }
        economy = 0
        comfort = 0
        driving_style = styl_jazdy_dict.get(self.styl_jazdy, None)

        mapped_przeznaczenie = przeznaczenie_dict.get(self.przeznaczenie, None)
        economy_list = mapped_przeznaczenie.copy()
        comfort_list = mapped_przeznaczenie.copy()
        if self.ekonomia == "bardzo" and len(mapped_przeznaczenie) > 2:
            economy_list = mapped_przeznaczenie[:-2]
            economy = 2
        elif self.ekonomia == "średnio" and len(mapped_przeznaczenie) > 1:
            economy_list = mapped_przeznaczenie[:-1]
            economy = 1

        if self.wygoda == "bardzo" and len(mapped_przeznaczenie) > 2:
            comfort_list = mapped_przeznaczenie[2:]
            comfort = 2
        elif self.wygoda == "średnio" and len(mapped_przeznaczenie) > 1:
            comfort_list = mapped_przeznaczenie[1:]
            comfort = 1

        common_part = set(economy_list) & set(comfort_list)
        if len(common_part) > 0:
            mapped_przeznaczenie = list(common_part)
        else:
            if len(mapped_przeznaczenie) % 2 == 0:
                mapped_przeznaczenie = mapped_przeznaczenie[len(mapped_przeznaczenie) // 2 - 1]
                mapped_przeznaczenie = list(mapped_przeznaczenie)
            else:
                mapped_przeznaczenie = mapped_przeznaczenie[len(mapped_przeznaczenie) // 2]
                mapped_przeznaczenie = list(mapped_przeznaczenie)

        with open('users.csv', 'r', encoding='utf-8') as file:
            id_usr = sum(1 for line in file)
            print("Liczba wierszy w pliku:", id_usr)

            self.id_usr = id_usr
            with open('users.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                row = str(id_usr) + ';' + str(self.przeznaczenie) + ';' + str(economy) + ';' + str(comfort) + ';' + str(
                    driving_style) + ';' + str(self.min_price) + ';' + str(self.max_price)
                writer.writerow([row])

        dec_user = DecodedUser(economy, comfort, driving_style, mapped_przeznaczenie, self.min_price, self.max_price, id_usr, self.przeznaczenie)
        return dec_user
