import json
import os
import time

import cv2

from etc.constants import FRAME_NAME, FONT_SMALL, FONT_XS, FONT_LARGE, FONT_NORMAL
from src.CustomExceptions import GameInterruptedException
from src.utils import display_non_blocking_message_top_center, display_non_blocking_message

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

    def show_stats(self, video, pseudo):
        timeout = time.time() + 10 #affichage pendant 10 secondes

        while time.time() < timeout:

            success, frame = video.read(0)

            if not success:
                raise RuntimeError("Erreur lecture vidéo pendant affichage des stats")

            frame = cv2.flip(frame, 1)

            display_non_blocking_message_top_center(frame, "Statistics")

            self.display_stats_player(frame, pseudo, (25, 200))
            self.display_stats_player(frame, "computer", (1050, 200))
            self.display_globals(frame, (500, 200))

            cv2.imshow(FRAME_NAME, frame)

            key = cv2.pollKey() & 0xFF
            if key == ord("q"):
                raise GameInterruptedException

    def display_stats_player(self, frame, pseudo, position):
        if pseudo not in self.data["players"]:
            self.data["players"][pseudo] = {}

        display_non_blocking_message(frame, pseudo, position=position, font=FONT_SMALL)

        properties = [("Wins", "games_won"),
                      ("Ties", "games_even"),
                      ("Losses", "games_lost"),
                      ("-", "-"),
                      ("Pierres", "pierre"),
                      ("Feuilles", "feuille"),
                      ("Ciseaux", "ciseaux"),
                      ("-", "-"),
                      ("Rounds won", "rounds_won"),
                      ("Rounds even", "rounds_even"),
                      ("Rounds lost", "rounds_lost")]
        position_gap = 50

        for prop in properties:
            if prop[0] == "-":
                position_gap += 30
                continue

            display_non_blocking_message(frame,
                                         f"{self.data['players'][pseudo].get(prop[1], 0)} {prop[0]}",
                                         position=(position[0], position[1] + position_gap),
                                         font=FONT_XS,
                                         font_color=(255, 0, 0))
            position_gap += 30

    def display_globals(self, frame, position):
        properties = [("Games played", "games_played"),
                      ("Games abandoned", "games_abandoned"),
                      ("Games ended in ties", "games_even"),
                      ("-", "-"),
                      ("Rounds expected to be played", "rounds_expected_to_be_played"),
                      ("Rounds really played", "rounds_played")]

        display_non_blocking_message(frame, "Global", position=position, font=FONT_NORMAL)

        position_gap = 50

        for prop in properties:
            if prop[0] == "-":
                position_gap += 30
                continue

            display_non_blocking_message(frame,
                                         f"{self.data.get(prop[1], 0)} {prop[0]}",
                                         position=(position[0], position[1] + position_gap),
                                         font=FONT_XS,
                                         font_color=(255, 0, 0))

            position_gap += 30

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
