from typing import Dict, List, Tuple
from intervals import HalfClosedIntervalLeft, Interval

import argparse
import csv
import pathlib


class WeightClass:
    def __init__(self, weight_classes_dict: Dict[Interval, Tuple[str, int]]):
        self._weight_classes: Dict[Interval] = weight_classes_dict
        self._div_list: List[Interval] = sorted(weight_classes_dict.keys(), reverse=True)
        self._curdiv = 0

    def division(self, weight: float) -> Tuple[str, int]:
        k = self._curdiv
        if weight in self._div_list[k]:
            return self._weight_classes[self._div_list[k]]

        if weight > self._div_list[k].upper_end:
            delta = -1
        else:
            delta = 1

        while True:
            k += delta
            if weight in self._div_list[k]:
                return self._weight_classes[self._div_list[k]]


boxing_weight_classes = {
    HalfClosedIntervalLeft(200, 750): ('Heavyweight', 200),  # technically unlimited upperbound
    HalfClosedIntervalLeft(175, 200): ('Cruiserweight', 175),
    HalfClosedIntervalLeft(168, 175): ('Light Heavyweight', 168),
    HalfClosedIntervalLeft(160, 168): ('Super Middleweight', 160),
    HalfClosedIntervalLeft(154, 160): ('Middleweight', 154),
    HalfClosedIntervalLeft(147, 154): ('Super Welterweight', 147),
    HalfClosedIntervalLeft(140, 147): ('Welterweight', 140),
    HalfClosedIntervalLeft(135, 140): ('Super Lightweight', 135),
    HalfClosedIntervalLeft(130, 135): ('Lightweight', 130),
    HalfClosedIntervalLeft(126, 130): ('Super Featherweight', 130),
    HalfClosedIntervalLeft(122, 130): ('Featherweight', 122),
    HalfClosedIntervalLeft(118, 122): ('Super Bantamweight', 118),
    HalfClosedIntervalLeft(115, 118): ('Bantamweight', 115),
    HalfClosedIntervalLeft(112, 115): ('Super Flyweight', 112),
    HalfClosedIntervalLeft(108, 112): ('Flyweight', 108)
}

body_set_weight_classes = {
    HalfClosedIntervalLeft(190, 195): ('O', 75),
    HalfClosedIntervalLeft(185, 190): ('N', 70),
    HalfClosedIntervalLeft(180, 185): ('M', 65),
    HalfClosedIntervalLeft(175, 180): ('L', 60),
    HalfClosedIntervalLeft(170, 175): ('K', 55),
    HalfClosedIntervalLeft(165, 170): ('J', 50),
    HalfClosedIntervalLeft(160, 165): ('I', 45),
    HalfClosedIntervalLeft(155, 160): ('H', 40),
    HalfClosedIntervalLeft(150, 155): ('G', 35),
    HalfClosedIntervalLeft(145, 150): ('F', 30),
    HalfClosedIntervalLeft(140, 145): ('E', 25),
    HalfClosedIntervalLeft(135, 140): ('D', 20),
    HalfClosedIntervalLeft(130, 135): ('C', 15),
    HalfClosedIntervalLeft(125, 130): ('B', 10),
    HalfClosedIntervalLeft(120, 125): ('A', 5),
}


def generate_body_mass_divisions(weights_csv_input: str, weights_division_csvpath: str):
    boxing_wd = WeightClass(boxing_weight_classes)
    body_set_weight_wd = WeightClass(body_set_weight_classes)

    with open(weights_csv_input, "r") as wfile, \
            open(weights_division_csvpath, "w") as dfile:
        rdr = csv.DictReader(wfile)
        wrtr = csv.DictWriter(dfile,
                              fieldnames=['date', 'Boxing Weight Class',
                                          'Boxing Weight Class Minimum', 'Body Set Weight Group',
                                          'Body Set Weight Minimum'])

        wrtr.writeheader()
        for row in rdr:
            w = float(row['bodymass'])
            box_div = boxing_wd.division(w)
            bsw_div = body_set_weight_wd.division(w)
            wrtr.writerow({
                    'date': row['date'],
                    'Boxing Weight Class': box_div[0],
                    'Boxing Weight Class Minimum': box_div[1],
                    'Body Set Weight Group': bsw_div[0],
                    'Body Set Weight Minimum': bsw_div[1]
            })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    weights_csvpath = f"{health_csv_folder}/{partition_date}/bodymass-summary.csv"
    weights_division_csvpath = \
        f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}/bodymass-divisions.csv"

    generate_body_mass_divisions(weights_csvpath, weights_division_csvpath)

