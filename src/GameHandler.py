import random

import cv2

from etc.constants import FEUILLE, PIERRE, CISEAUX, FRAME_NAME, COMPUTER_WIN, PLAYER_WIN
from src.Landmarks import Landmarks, get_landmarks
from src.utils import display_blocking_message_center, display_non_blocking_message_top_left, \
    display_non_blocking_message_bottom_left


class GameHandler:

    def __init__(self, video):
        self.video = video
        self.draw = False

    def initialize_game(self):
        print("Début de la partie, saisie nombre de rounds")
        number_of_rounds = 0
        key = False
        last_gesture = None  # mémoire pour dernière gesture reconnue
        last_gesture_sum = 0  # Nombre de fois qu'on a eu la même gesture d'affilé
        number_of_frames_to_validate = 20

        while (key != ord("q")) and (last_gesture_sum < number_of_frames_to_validate or not number_of_rounds or number_of_rounds < 1):
            success, frame = self.video.read(0)

            if not success:
                print("Erreur lecture vidéo pendant l'acquisition du nombre de tours")
                break

            frame = cv2.flip(frame, 1)

            # Faire le traitement et les modifications d'images ici
            # Landmarks' keypoints coordinates (0,0) is top left, (1,1) is bottom right
            frame, landmarks = get_landmarks(frame, self.draw)
            number_of_rounds = self.get_number_of_rounds_posture(landmarks)

            if number_of_rounds == last_gesture:
                last_gesture_sum += 1
            else:
                last_gesture_sum = 0

            if number_of_rounds:
                display_non_blocking_message_bottom_left(frame, f"{last_gesture_sum} / {number_of_frames_to_validate}")

            last_gesture = number_of_rounds

            display_non_blocking_message_top_left(frame, f"Nombre de rounds : {number_of_rounds}")

            cv2.imshow(FRAME_NAME, frame)

            key = cv2.pollKey() & 0xFF
            if key == ord("d"):
                self.draw = not self.draw

        if number_of_rounds:
            display_blocking_message_center(self.video, f"C'est parti pour {number_of_rounds} rounds !", 25,
                                            font_color=(255, 0, 0))
            self.start_game(number_of_rounds)

    def get_number_of_rounds_posture(self, landmarks: Landmarks):
        """
        Return the number of stretched fingers corresponding to the numbers of rounds.

        The hand has to be correctly oriented (top of fingers towards the
        top of the image from woth the landmarks has been extracted).
        Works if it's either the hand palm facing the camera or the back of the hand.

        If the landmarks object attribute containing the keypoints is None,
        (i.e. no hand detected) the function returns None.

        Parameters
        ----------
        landmarks -- The landmarks object of the hand for which we want to count the fingers

        Return
        ------
        an int -- the number of stretched fingers
        """

        if not landmarks.is_not_none():
            return None

        # Determine if it's the palm or the back that is facing the camera
        # in order to choose the condition determining if the thumb is stretched or not
        palm_facing_camera = landmarks.get_keypoint_x(5) < landmarks.get_keypoint_x(17)

        if palm_facing_camera:
            thumb_up = landmarks.get_keypoint_x(4) < landmarks.get_keypoint_x(2)
        else:
            thumb_up = landmarks.get_keypoint_x(4) > landmarks.get_keypoint_x(2)

        index_up = landmarks.get_keypoint_y(8) < landmarks.get_keypoint_y(6)
        middle_up = landmarks.get_keypoint_y(12) < landmarks.get_keypoint_y(10)
        ring_up = landmarks.get_keypoint_y(16) < landmarks.get_keypoint_y(14)
        pinky_up = landmarks.get_keypoint_y(20) < landmarks.get_keypoint_y(18)
        return thumb_up + index_up + middle_up + ring_up + pinky_up

    def get_user_game_posture(self, landmarks: Landmarks):
        """
        Return the symbol made by the hand on the image
        which is an element of POSSIBLE_GAME_POSTURES.
        """

        if not landmarks.is_not_none():
            return None

        # Determine if it's the palm or the back that is facing the camera
        # in order to choose the condition determining if the thumb is stretched or not
        palm_facing_camera = landmarks.get_keypoint_x(5) < landmarks.get_keypoint_x(17)

        if palm_facing_camera:
            thumb_up = landmarks.get_keypoint_x(4) < landmarks.get_keypoint_x(2)
        else:
            thumb_up = landmarks.get_keypoint_x(4) > landmarks.get_keypoint_x(2)

        index_up = landmarks.get_keypoint_y(8) < landmarks.get_keypoint_y(6)
        middle_up = landmarks.get_keypoint_y(12) < landmarks.get_keypoint_y(10)
        ring_up = landmarks.get_keypoint_y(16) < landmarks.get_keypoint_y(14)
        pinky_up = landmarks.get_keypoint_y(20) < landmarks.get_keypoint_y(18)
            
        feuille1 = abs(landmarks.get_keypoint_y(6) - landmarks.get_keypoint_y(8))<0.05
        feuille2 = abs(landmarks.get_keypoint_y(10) - landmarks.get_keypoint_y(12))<0.05
        feuille3 = abs(landmarks.get_keypoint_y(14) - landmarks.get_keypoint_y(16)) <0.05
        feuille4 = abs(landmarks.get_keypoint_y(18) - landmarks.get_keypoint_y(20)) <0.05
        feuille5 = abs(landmarks.get_keypoint_y(4) - landmarks.get_keypoint_y(3)) <0.05
        feuille6 = abs(landmarks.get_keypoint_x(6) - landmarks.get_keypoint_x(20)) >0.07
        feuille7 = abs(landmarks.get_keypoint_x(4) - landmarks.get_keypoint_x(10))>0.04
        
        
        cis1 = abs(landmarks.get_keypoint_x(6) - landmarks.get_keypoint_x(8))< 0.07
        cis2 = abs(landmarks.get_keypoint_x(10) - landmarks.get_keypoint_x(12))< 0.07
        cis3 = abs(landmarks.get_keypoint_x(14) - landmarks.get_keypoint_x(16)) < 0.07
        cis4 = abs(landmarks.get_keypoint_x(18) - landmarks.get_keypoint_x(20)) < 0.07
        cis5 = abs(landmarks.get_keypoint_x(14) - landmarks.get_keypoint_x(13)) > 0.03
        cis6 = abs(landmarks.get_keypoint_x(18) - landmarks.get_keypoint_x(17))> 0.03
        cis7 = abs(landmarks.get_keypoint_x(8) - landmarks.get_keypoint_x(20))>0.01
        cis8 = abs(landmarks.get_keypoint_y(4) - landmarks.get_keypoint_y(10))>0.05
        
        pierre1 = abs(landmarks.get_keypoint_x(5) > landmarks.get_keypoint_x(6))
        pierre2 = abs(landmarks.get_keypoint_x(9) > landmarks.get_keypoint_x(10))
        pierre3 = abs(landmarks.get_keypoint_x(13) > landmarks.get_keypoint_x(14))
        pierre4 = abs(landmarks.get_keypoint_x(17) > landmarks.get_keypoint_x(18))
        pierre5 = abs(landmarks.get_keypoint_y(4) - landmarks.get_keypoint_y(10))<0.02 or abs(landmarks.get_keypoint_x(4) - landmarks.get_keypoint_x(6))<0.02

        if (feuille1 and feuille2 and feuille3 and feuille4 and feuille5 and feuille6 and feuille7) :
            return FEUILLE
        if (index_up and middle_up) or (cis1 and cis2 and cis3 and cis4 and cis5  and cis6 and cis7 and cis8) :
            return CISEAUX
        if (pierre1 and pierre2 and pierre3 and pierre4 and pierre5):
            return PIERRE


    def start_game(self, number_of_rounds):
        key = False
        rounds_played = 0
        player_rounds_won = 0
        computer_won_rounds = 0
        number_of_frames_to_validate = 20
        while key != ord("q") and rounds_played < number_of_rounds:
            
            last_gesture = None  # mémoire pour dernière gesture reconnue
            posture_player = None
            last_gesture_sum = 0  # Nombre de fois qu'on a eu la même gesture d'affilé
            display_blocking_message_center(self.video, f"Round {rounds_played + 1} / {number_of_rounds}", 25,
                                            font_color=(255, 0, 0))
            print("ROUND ", rounds_played +1)
            
            while (last_gesture_sum < number_of_frames_to_validate): 

               success, frame = self.video.read(0)

               if not success:
                    print("Erreur lecture vidéo pendant l'acquisition de la posture")
                    break

               frame = cv2.flip(frame, 1)
               
               # Faire le traitement et les modifications d'images ici
               # Landmarks' keypoints coordinates (0,0) is top left, (1,1) is bottom right
               frame, landmarks = get_landmarks(frame, self.draw)

               posture_player = self.get_user_game_posture(landmarks)
              
               if (posture_player == last_gesture and posture_player != None):
                    last_gesture_sum += 1
               else:
                    last_gesture_sum = 0

               if (posture_player != None):
                   display_non_blocking_message_bottom_left(frame, f"{last_gesture_sum} / {number_of_frames_to_validate}")
                    
               last_gesture = posture_player
                
               display_non_blocking_message_top_left(frame, f"Posture detectee : {posture_player}")
               
               cv2.imshow(FRAME_NAME, frame)
               
               key = cv2.pollKey() & 0xFF
               if key == ord("d"):
                self.draw = not self.draw
                
            if posture_player :
            
                display_blocking_message_center(self.video, f"Acquisition humain : {posture_player}", 15)

            posture_computer = self.get_computer_game_posture()

            display_blocking_message_center(self.video, f"Posture ordi : {posture_computer}", 25)

            winner = self.get_winner(posture_player, posture_computer)

            if winner == PLAYER_WIN:
                display_blocking_message_center(self.video,
                                                      f"Bravo ! Tu remportes le round ({posture_player} > {posture_computer})",
                                                25,
                                                font_size=1,
                                                font_stroke=2)
                player_rounds_won = player_rounds_won + 1
            elif winner == COMPUTER_WIN:
                display_blocking_message_center(self.video,
                                                      f"Dommage, l'ordinateur remporte le round ({posture_computer} > {posture_player})",
                                                25,
                                                font_size=1,
                                                font_stroke=2)
                computer_won_rounds = computer_won_rounds + 1
            else:
                display_blocking_message_center(self.video, f"Match nul ! Aucun gagnant ce round", 25)

            rounds_played = rounds_played + 1

            key = cv2.pollKey() & 0xFF

        if player_rounds_won > computer_won_rounds:
            display_blocking_message_center(self.video,
                                                  f"Victoire {player_rounds_won} rounds a {computer_won_rounds} !", 50,
                                            font_color=(0, 255, 0))
        elif computer_won_rounds > player_rounds_won:
            display_blocking_message_center(self.video,
                                                  f"Defaite {player_rounds_won} rounds a {computer_won_rounds} ...", 50,
                                            font_color=(0, 0, 255))
        else:
            display_blocking_message_center(self.video,
                                                  f"Egalite ! Aucun gagnant cette fois-ci...",
                                            50,
                                            font_color=(255, 0, 0))

    def get_computer_game_posture(self):
        return random.choice([FEUILLE, PIERRE, CISEAUX])

    def get_winner(self, posture_player, posture_computer):
        if posture_computer == posture_player:
            return None

        better_posture = self.get_better_posture(posture_player)

        if posture_computer == better_posture:
            return COMPUTER_WIN

        return PLAYER_WIN

    def get_better_posture(self, posture):
        if posture == FEUILLE:
            return CISEAUX

        if posture == PIERRE:
            return FEUILLE

        return PIERRE
