import random
import time

import cv2

from etc.constants import FEUILLE, FEUILLE_THRESHOLD, PIERRE, CISEAUX, FRAME_NAME, COMPUTER_WIN, PLAYER_WIN, \
    CISEAUX_THRESHOLD, FONT_SMALL, FONT_NORMAL, FONT_XS
from src.CustomExceptions import GameInterruptedException
from src.Landmarks import Landmarks, get_landmarks
from src.StatisticsHandler import StatisticsHandler
from src.utils import display_blocking_message_center, display_non_blocking_message_top_left, \
    display_non_blocking_message_bottom_center, get_number_stretched_fingers, display_non_blocking_message, \
    display_non_blocking_message_center


class GameHandler:

    def __init__(self, video, player, statistics_handler: StatisticsHandler):
        self.video = video
        self.draw = False
        self.player = player
        self.statistics_handler = statistics_handler
        self.player_rounds_won = 0
        self.computer_rounds_won = 0
        self.rounds_played = []

    def add_round_played(self, winner, posture_player, posture_computer):
        self.rounds_played.append({
            "winner": winner,
            "posture_player": posture_player,
            "posture_computer": posture_computer
        })

    def initialize_game(self):
        """
            Initialize the game by getting the number of rounds needed, printing a message and launching the game
        """
        self.statistics_handler.increment_global_stats("games_played")
        number_of_rounds = self.get_number_of_rounds()
        display_blocking_message_center(self.video, f"C'est parti pour {number_of_rounds} rounds !", seconds=3,
                                        font_color=(255, 0, 0))
        self.start_game(number_of_rounds)

    def get_number_of_rounds(self):
        """"
            Loop while the user hasnt shown a valid posture for more than X frames,
            return an integer between 1 and 5
        """
        number_of_rounds = 0
        last_gesture = None  # mémoire pour dernière gesture reconnue
        last_gesture_sum = 0  # Nombre de fois qu'on a eu la même gesture d'affilé
        number_of_frames_to_validate = 20
        while last_gesture_sum < number_of_frames_to_validate or not number_of_rounds or number_of_rounds < 1:
            success, frame = self.video.read(0)

            if not success:
                raise RuntimeError("Erreur lecture vidéo pendant l'acquisition du nombre de tours")

            frame = cv2.flip(frame, 1)

            # Faire le traitement et les modifications d'images ici
            # Landmarks' keypoints coordinates (0,0) is top left, (1,1) is bottom right
            frame, landmarks = get_landmarks(frame, self.draw)
            number_of_rounds = self.recognize_number_of_rounds_posture(landmarks)

            if number_of_rounds == last_gesture:
                last_gesture_sum += 1
            else:
                last_gesture_sum = 0

            if number_of_rounds:
                display_non_blocking_message_bottom_center(frame,
                                                           f"{last_gesture_sum} / {number_of_frames_to_validate}")

            last_gesture = number_of_rounds

            display_non_blocking_message_top_left(frame, f"Nombre de rounds : {number_of_rounds}")

            cv2.imshow(FRAME_NAME, frame)

            key = cv2.pollKey() & 0xFF
            if key == ord("d"):
                self.draw = not self.draw
            elif key == ord("q"):
                raise GameInterruptedException

        self.statistics_handler.increment_global_stats("rounds_expected_to_be_played", number_of_rounds)
        return number_of_rounds

    def recognize_number_of_rounds_posture(self, landmarks: Landmarks):
        """
        Return the number of stretched fingers corresponding to the numbers of rounds.

        See get_number_stretched_fingers for more details

        If the landmarks object attribute containing the keypoints is None,
        (i.e. no hand detected) the function returns None.

        Parameters
        ----------
        landmarks -- The landmarks object of the hand for which we want to count the fingers

        Return
        ------
        an int -- the number of stretched fingers (in [0,5])
        """

        if not landmarks.is_not_none():
            return None
        return get_number_stretched_fingers(landmarks)

    def get_user_posture(self):
        """
            Loop while the user hasnt shown a valid posture between Rock Paper and Scissors
            returns an integer corresponding to the posture chosen (see etc/constants.py)
        """
        last_gesture = None  # mémoire pour dernière gesture reconnue
        posture_player = None
        last_gesture_sum = 0  # Nombre de fois qu'on a eu la même gesture d'affilé
        number_of_frames_to_validate = 10

        while last_gesture_sum < number_of_frames_to_validate:

            success, frame = self.video.read(0)

            if not success:
                raise RuntimeError("Erreur lecture vidéo pendant l'acquisition de la posture")

            frame = cv2.flip(frame, 1)

            # Faire le traitement et les modifications d'images ici
            # Landmarks' keypoints coordinates (0,0) is top left, (1,1) is bottom right
            frame, landmarks = get_landmarks(frame, self.draw)

            self.display_rounds_live_result(frame)

            posture_player = self.recognize_user_game_posture(landmarks)

            if posture_player == last_gesture and posture_player is not None:
                last_gesture_sum += 1
            else:
                last_gesture_sum = 0

            if posture_player is not None:
                display_non_blocking_message_bottom_center(frame,
                                                           f"{last_gesture_sum} / {number_of_frames_to_validate}")

            last_gesture = posture_player

            display_non_blocking_message_top_left(frame, f"Posture detectee : {posture_player}")

            cv2.imshow(FRAME_NAME, frame)

            key = cv2.pollKey() & 0xFF
            if key == ord("d"):
                self.draw = not self.draw
            if key == ord("q"):
                raise GameInterruptedException

        return posture_player

    def recognize_user_game_posture(self, landmarks: Landmarks):
        """
        Return the symbol made by the hand on the image
        which is an element of POSSIBLE_GAME_POSTURES.

        Parameters
        ----------
        landmarks -- The landmarks object of the hand for which we want to recognize the posture

        Return
        ------
        a String -- The recognized game posture (CISEAUX, PIERRE or FEUILLE) or None if 
            no game posture is recognized
        """

        if not landmarks.is_not_none():
            return None

        index_up = landmarks.get_distance_between(0, 8) > landmarks.get_distance_between(0, 6)
        middle_up = landmarks.get_distance_between(0, 12) > landmarks.get_distance_between(0, 10)
        ring_up = landmarks.get_distance_between(0, 16) > landmarks.get_distance_between(0, 14)
        pinky_up = landmarks.get_distance_between(0, 20) > landmarks.get_distance_between(0, 18)

        # The posture is a CISEAUX if the space between keypoint 8 and 12 
        # is wider than the space between 5 and 9
        # and if ring and pinky fingers aren't stretched
        distance_top_fingers = landmarks.get_distance_between(8, 12)
        distance_bottom_fingers = landmarks.get_distance_between(5, 9)
        is_ciseaux = not ring_up and not pinky_up and index_up and middle_up and distance_top_fingers > CISEAUX_THRESHOLD * distance_bottom_fingers
        if (is_ciseaux):
            return CISEAUX

        # The posture is a PIERRE if is all fingers aren't stretched
        # (thumb isn't stretched if keypoint 4 is "close" to 10)
        thumb_close_to_middle = landmarks.get_distance_between(4, 10) < landmarks.get_distance_between(1, 2)
        is_pierre = not index_up and not middle_up and not ring_up and not pinky_up and thumb_close_to_middle
        if is_pierre:
            return PIERRE

        # The posture is a FEUILLE if the distance between keypoint 6 and 19 is close to 5 and 17
        distance_stuck_fingers1 = landmarks.get_distance_between(7, 20)
        distance_stuck_fingers2 = landmarks.get_distance_between(5, 17)
        finger_stuck = distance_stuck_fingers1 < FEUILLE_THRESHOLD * distance_stuck_fingers2
        is_feuille = finger_stuck and index_up and middle_up and ring_up and pinky_up
        if is_feuille:
            return FEUILLE

        # Return None if no game posture has been recognized
        return None

    def start_game(self, number_of_rounds):
        """
            Loops for number_of_rounds rounds, each round consists in the player choosing a posture, the computer then
            choosing one, and comparing the two to display the winner
        """
        self.rounds_played = []
        self.player_rounds_won = 0
        self.computer_rounds_won = 0

        while len(self.rounds_played) < number_of_rounds:

            posture_player, posture_computer = self.get_round_postures(number_of_rounds)

            winner = self.get_winner(posture_player, posture_computer)

            self.add_round_played(winner, posture_player, posture_computer)  # bien faire avant display round winner

            if winner == PLAYER_WIN:
                self.player_rounds_won += 1
            elif winner == COMPUTER_WIN:
                self.computer_rounds_won += 1

            self.display_round_winner(winner, posture_player, posture_computer)

            self.statistics_handler.increment_global_stats("rounds_played")

            key = cv2.pollKey() & 0xFF
            if key == ord("q"):
                raise GameInterruptedException

        if self.player_rounds_won > self.computer_rounds_won:
            display_blocking_message_center(self.video,
                                            f"Victoire {self.player_rounds_won} rounds a {self.computer_rounds_won} !",
                                            seconds=4,
                                            font_color=(0, 255, 0))
            self.statistics_handler.increment_stats_player(self.player, "games_won")
            self.statistics_handler.increment_stats_player("computer", "games_lost")

        elif self.computer_rounds_won > self.player_rounds_won:
            display_blocking_message_center(self.video,
                                            f"Defaite {self.player_rounds_won} rounds a {self.computer_rounds_won} ...",
                                            seconds=4,
                                            font_color=(0, 0, 255))
            self.statistics_handler.increment_stats_player("computer", "games_won")
            self.statistics_handler.increment_stats_player(self.player, "games_lost")
        else:
            display_blocking_message_center(self.video,
                                            f"Egalite ! Aucun gagnant cette fois-ci...",
                                            seconds=4,
                                            font_color=(255, 0, 0))
            self.statistics_handler.increment_global_stats("games_even")
            self.statistics_handler.increment_stats_player(self.player, "games_even")
            self.statistics_handler.increment_stats_player("computer", "games_even")

        self.log_rounds_to_stats(self.player)
        self.log_rounds_to_stats("computer")
        self.statistics_handler.write_stats()

    def log_rounds_to_stats(self, player):
        """
            Add this game statistics to the statistics module
        """
        self.statistics_handler.increment_stats_player(player, "rounds_won", self.player_rounds_won)
        self.statistics_handler.increment_stats_player(player, "rounds_lost", self.computer_rounds_won)
        self.statistics_handler.increment_stats_player(player, "rounds_even",
                                                       len(self.rounds_played) - self.player_rounds_won - self.computer_rounds_won)

    def get_round_postures(self, number_of_rounds):
        """
            Asks for the posture player and then chooses one for the computer, while displaying what happened every time
        """
        display_blocking_message_center(self.video, f"Round {len(self.rounds_played) + 1} / {number_of_rounds}",
                                        seconds=2,
                                        font_color=(255, 0, 0))

        posture_player = self.get_user_posture()

        display_blocking_message_center(self.video, f"Acquisition humain : {posture_player}", seconds=2)

        posture_computer = self.get_computer_game_posture()

        display_blocking_message_center(self.video, f"Posture ordi : {posture_computer}", seconds=2)

        self.statistics_handler.increment_stats_player("computer", posture_computer)
        self.statistics_handler.increment_stats_player(self.player, posture_player)

        return posture_player, posture_computer

    def get_computer_game_posture(self):
        """
            Returns the gesture chosen by the computer
        """
        return random.choice([FEUILLE, PIERRE, CISEAUX])

    def get_winner(self, posture_player, posture_computer):
        """
            Compares two posture and returns the winner or None
        """
        if posture_computer == posture_player:
            return None

        better_posture = self.get_better_posture(posture_player)

        if posture_computer == better_posture:
            return COMPUTER_WIN

        return PLAYER_WIN

    def get_better_posture(self, posture):
        """
            Gets a posture and returns the better posture
        """
        if posture == FEUILLE:
            return CISEAUX

        if posture == PIERRE:
            return FEUILLE

        return PIERRE

    def display_rounds_live_result(self, frame):
        base_y = frame.shape[0] - 25
        img_size = 50

        for index, round_stats in enumerate(self.rounds_played):

            display_non_blocking_message(frame, f"{index + 1}", position=(148, base_y - 35), font=FONT_XS)

            if round_stats["posture_player"] == round_stats["posture_computer"]:
                display_non_blocking_message(frame, "Nul", position=(130, base_y - 5), font=FONT_SMALL,
                                             font_color=(255, 0, 0))
            elif self.get_better_posture(round_stats["posture_computer"]) == round_stats["posture_player"]:
                display_non_blocking_message(frame, "Victoire", position=(90, base_y - 5), font=FONT_SMALL,
                                             font_color=(0, 255, 0))
            else:
                display_non_blocking_message(frame, "Defaite", position=(95, base_y - 5), font=FONT_SMALL,
                                             font_color=(0, 0, 255))

            img_path_player = f"img/{round_stats['posture_player']}.png"
            image_player = cv2.resize(cv2.imread(img_path_player), (img_size, img_size))

            img_path_computer = f"img/{round_stats['posture_computer']}.png"
            image_computer = cv2.resize(cv2.imread(img_path_computer), (img_size, img_size))

            frame[base_y - img_size:base_y, 25:25 + img_size] = image_player
            frame[base_y - img_size:base_y, 225:225 + img_size] = image_computer

            base_y -= 85

    def display_round_winner(self, winner, posture_player, posture_computer):
        seconds = 3

        timeout = time.time() + seconds

        while time.time() < timeout:

            success, frame = self.video.read(0)

            if not success:
                raise RuntimeError("Erreur lecture vidéo pendant affichage vainqueur du round")

            frame = cv2.flip(frame, 1)

            if winner == PLAYER_WIN:
                display_non_blocking_message_center(frame, f"Bravo !", font_color=(0, 255, 0), y_offset=-20)
                display_non_blocking_message_center(frame, f"Tu remportes le round", y_offset=50, font=FONT_NORMAL)
                display_non_blocking_message_center(frame,
                                                    f"({posture_player.capitalize()} > {posture_computer.capitalize()})",
                                                    y_offset=100, font=FONT_SMALL)

            elif winner == COMPUTER_WIN:
                display_non_blocking_message_center(frame, f"Dommage", font_color=(0, 0, 255), y_offset=-20)
                display_non_blocking_message_center(frame, f"L'ordinateur remporte le round", y_offset=50,
                                                    font=FONT_NORMAL)
                display_non_blocking_message_center(frame,
                                                    f"({posture_player.capitalize()} < {posture_computer.capitalize()})",
                                                    y_offset=100, font=FONT_SMALL)

            else:
                display_non_blocking_message_center(frame, f"Match nul", font_color=(255, 0, 0), y_offset=-20)
                display_non_blocking_message_center(frame, f"Aucun gagnant ce round", y_offset=75, font=FONT_NORMAL)

            self.display_rounds_live_result(frame)

            cv2.imshow(FRAME_NAME, frame)

            key = cv2.pollKey() & 0xFF
            if key == ord("q"):
                raise GameInterruptedException
