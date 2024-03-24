class DecodedUser:
    def __init__(self, economy, comfort, driving_style, purpose):
        self.purpose = purpose
        self.driving_style = driving_style
        self.comfort = comfort
        self.economy = economy


class User:
    def __init__(self, przeznaczenie, ekonomia, wygoda, styl_jazdy):
        self.styl_jazdy = styl_jazdy
        self.wygoda = wygoda
        self.ekonomia = ekonomia
        self.przeznaczenie = przeznaczenie

    def decode(self):
        przeznaczenie_dict ={
            'Rodzinny': ['D', 'E', 'K'],
            'Miejski': ['A', 'B', 'C'],
            'Uniwersalny': ['C', 'D', 'E'],
            'Trasy': ['D', 'E', 'F', 'K'],
            'Sportowy': ['G'],
        }
        styl_jazdy_dict ={
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

        dec_user = DecodedUser(economy, comfort, driving_style, mapped_przeznaczenie)
        return dec_user