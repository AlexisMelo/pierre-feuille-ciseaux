import json
from pprint import pprint
import os

default_dict = {
    "games_played": 0,
    "games_abandoned": 0,
    "players": {},
    "rounds_expected_to_be_played": 0
}


class StatisticsHandler:

    def __init__(self):
        self.stats_folder = "var"
        self.stats_file_name = "stats.json"
        self.stats_path = f"{self.stats_folder}/{self.stats_file_name}"

        self.data = default_dict

        if not os.path.exists(self.stats_path):
            print(f"Création fichier {self.stats_path}")
            if not os.path.exists(self.stats_folder):
                os.makedirs(self.stats_folder)

            with open(self.stats_path, "w") as file:
                json.dump(default_dict, file, indent=4, sort_keys=True, ensure_ascii=False)

        self.data = self.read_stats()

    def show_stats(self, pseudo):
        print("affichage des stats")
        pprint(self.data)

    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def read_stats(self):
        print(f"Lecture des données de {self.stats_path}")
        with open(self.stats_path) as json_file:
            try:
                data = json.load(json_file)
                if not data:
                    data = default_dict
            except Exception:
                data = default_dict
            return data

    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def write_stats(self):
        print(f"Écriture des données dans {self.stats_path}")
        with open(self.stats_path, 'w+') as outfile:
            json.dump(self.data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    def increment_stats_player(self, player, stat_name, value=1):
        if player not in self.data["players"]:
            self.data["players"][player] = {
                stat_name: 0
            }

        if stat_name not in self.data["players"][player]:
            self.data["players"][player][stat_name] = 0

        self.data["players"][player][stat_name] = self.data["players"][player][stat_name] + value

    def increment_global_stats(self, stat_name, value=1):
        if stat_name not in self.data:
            self.data[stat_name] = 0

        self.data[stat_name] = self.data[stat_name] + value
