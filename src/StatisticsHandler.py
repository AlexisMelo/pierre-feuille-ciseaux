import json
from pprint import pprint


class StatisticsHandler:

    def __init__(self, video):
        self.video = video
        self.draw = False
        self.stats_path = "var/stats.json"

    def show_stats(self, pseudo):
        print("affichage des stats")
        stats = self.read_stats()
        print(stats)
        if "bidule" in stats:
            stats["bidule"]["machin"] = stats["bidule"]["machin"] + 1
        else:
            stats["bidule"] = {
                "machin": 1,
                "aaaaaaaa": "eeeee"
            }
        self.write_stats(stats)

    #https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def read_stats(self):
        print("Lecture des données...")
        with open(self.stats_path) as json_file:
            data = json.load(json_file)
            pprint(data)
            return data

    #https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    def write_stats(self, stats_dict=None):
        if stats_dict is None:
            stats_dict = {}
        print("Écriture des données...")
        with open(self.stats_path, 'w+') as outfile:
            json.dump(stats_dict, outfile, indent=4, sort_keys=True, ensure_ascii=False)