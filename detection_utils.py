import cv2
import numpy as np
from constants import *
import mediapipe as mp


#################################
## THE 3 RECOGNITION FUNCTIONS ##
#################################


def get_user_game_posture(img):
    """
    Return the symbol made by the hand on the image
    which is an element of POSSIBLE_GAME_POSTURES.
    """
    pass


def get_number_of_rounds_posture(img):
    """
    Return an integer : the number of stretched fingers
    corresponding to the numbers of rounds.
    """
    pass


def get_starting_gesture(img):
    """
    Return the gesture made by the hand on the image
    which is an element of POSSIBLE_GESTURES
    Code obtained from https://google.github.io/mediapipe/solutions/hands
    """
    pass


def get_landmarks(img):
    """
    Code obtained from https://google.github.io/mediapipe/solutions/hands
    """

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

        # Draw the hand annotations on the img.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

        # Flip the image horizontally for a selfie-view display.
        return cv2.flip(img, 1)
