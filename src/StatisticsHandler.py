import json
from pprint import pprint

default_dict = {
    "games_played": 0,
    "games_abandoned": 0,
    "players": {
        # "computer": {
        #  "rounds_won": 0,
        #  "rounds_played": 0,
        #  "scissor": 0,
        #  "rock": 0,
        #  "paper": 0
        # }
    }
}


class StatisticsHandler:

    def __init__(self):
        self.stats_path = "var/stats.json"

    def show_stats(self, pseudo):
        print("affichage des stats")
        stats = self.read_stats()
        pprint(stats)
        self.write_stats(stats)

    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def read_stats(self):
        print("Lecture des données...")
        with open(self.stats_path) as json_file:
            data = json.load(json_file)
            if not data:
                data = default_dict
            return data

    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def write_stats(self, stats_dict=None):
        if stats_dict is None:
            stats_dict = default_dict
        print("Écriture des données...")
        with open(self.stats_path, 'w+') as outfile:
            json.dump(stats_dict, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    def increment_stats_player(self, player, stat_name, value=1):
        stats = self.read_stats()
        if player not in stats.players:
            stats.players[player] = {
                stat_name: 0
            }

        if stat_name not in stats.players[player]:
            stats.players[player][stat_name] = 0

        stats.players[player][stat_name] = stats.players[player][stat_name] + value

        self.write_stats(stats)

    def increment_global_stats(self, stat_name, value=1):
        stats = self.read_stats()
        if stat_name not in stats:
            stats[stat_name] = 0

        stats[stat_name] = stats[stat_name] + value
        self.write_stats(stats)
