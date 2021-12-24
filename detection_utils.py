import cv2
import numpy as np
from Memory import Memory
from Landmarks import Landmarks
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
    return FEUILLE


def get_number_of_rounds_posture(landmarks: Landmarks):
    """
    Return an integer : the number of stretched fingers
    corresponding to the numbers of rounds.
    """

    if landmarks.is_not_none():
        thumb_up = landmarks.get_keypoint_x(4) < landmarks.get_keypoint_x(2)
        index_up = landmarks.get_keypoint_y(8) < landmarks.get_keypoint_y(6)
        middle_up = landmarks.get_keypoint_y(12) < landmarks.get_keypoint_y(10)
        ring_up = landmarks.get_keypoint_y(16) < landmarks.get_keypoint_y(14)
        pinky_up = landmarks.get_keypoint_y(20) < landmarks.get_keypoint_y(18)
        return thumb_up + index_up + middle_up + ring_up + pinky_up
    else:
        return None


def get_starting_gesture(memory: Memory):
    """
    Return the gesture made by the hand on the image
    which is an element of POSSIBLE_GESTURES
    Code obtained from https://google.github.io/mediapipe/solutions/hands
    """
    if memory:
        return memory.recognize_starting_gesture()
    else:
        return None


def get_landmarks(img, draw=False):
    """Get the landmarks of the hand if present in img.

    Extract the landmarks of 1 or 2 hands on img. Landmaks are described in
    https://google.github.io/mediapipe/solutions/hands.html

    Parameters
    ----------
    img -- the image to hand landmarks from
    draw -- a boolean to draw or not the detected landmarks on img (default False)

    Return
    ------
    img -- the same image as img but with landmarks if draw==True
    Landmarks(dict_landmarks_coordinates) -- a Landmarks object intialized with
        a dict containing the landmarks (may be None)

    Note
    ----
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
        dict_landmarks_coordinates = None

        # Draw the hand annotations on the img.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            # Draw the "skeleton" if needed
            if draw:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )

            # Create a list of all the (x,y) normalized coordinates of the landmarks
            # e.g. [(0.1251,0.1994), (0.1513,0.9482), ...]
            list_coordinates = [
                (data_point.x, data_point.y)
                for data_point in results.multi_hand_landmarks[0].landmark
            ]

            # Create a dict to map keypoints ids (0 to 20) to their normalized (x,y) coordinates in img
            # e.g. {0: (0.1251,0.1994), 1: (0.1513,0.9482), ..., 20: (0.8461,0.7138)}
            # (0,0) being top left and (1,1) bottom right
            # See https://google.github.io/mediapipe/solutions/hands.html for more details
            dict_landmarks_coordinates = {
                i: pos for i, pos in zip(range(21), list_coordinates)
            }

        return img, Landmarks(dict_landmarks_coordinates)
