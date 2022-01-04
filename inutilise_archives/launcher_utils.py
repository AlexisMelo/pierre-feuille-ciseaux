import cv2
import image_utils as iu
from etc.constants import *
from random import randint


def run_app():
    # define a video capture object (0 = default webcam)
    vid = cv2.VideoCapture(0)

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read(0)

        # Faire le traitement et les modifications d'images ici
        # e.g. : frame = iu.write_score(frame)
        start_gesture = du.get_starting_gesture(frame)
        if start_gesture == LAUNCH_GAME:
            nb_rounds = du.recognize_number_of_rounds_posture(frame)
            cpt = 0
            while cpt < nb_rounds:
                posture_player = du.recognize_user_game_posture(frame)
                posture_computer = get_computer_game_posture()
                frame = iu.display_computer_game_posture(frame, posture_computer)
                #cv2.waitKey(1) pour attendre
                winner = get_winner(posture_player, posture_computer)
                frame = iu.display_winner_or_round(frame, winner)
                #cv2.waitKey(1) pour attendre
                cpt += 1
            #frame = iu.display_final_winner(frame, winner, " 5-3")
        elif start_gesture == STATISTICS:
            #frame = iu.display_scores_previous_games(frame,scores) #score doit etre une liste ex : ["5-3","4-2","3-1","3-0"]
            pass

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # Press 'q' to quit
        key = cv2.pollKey() & 0xFF
        if key == ord("q"):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def get_winner(posture_player, posture_computer):
    win_gesture = get_gesture_winner(posture_player, posture_computer)
    if win_gesture == posture_player:
        return PLAYER_WIN
    else:
        return COMPUTER_WIN


def get_gesture_winner(g1, g2):
    if (g1 == CISEAUX and g2 == PIERRE) or (g2 == CISEAUX and g1 == PIERRE):
        return PIERRE
    elif (g1 == CISEAUX and g2 == FEUILLE) or (g2 == CISEAUX and g1 == FEUILLE):
        return CISEAUX
    elif (g1 == PIERRE and g2 == FEUILLE) or (g2 == PIERRE and g1 == FEUILLE):
        return FEUILLE


def get_computer_game_posture():
    random = randint(0, 2)
    if random == 0: return CISEAUX
    if random == 1: return PIERRE
    if random == 2: return FEUILLE
