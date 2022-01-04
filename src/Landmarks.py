import mediapipe as mp
import cv2
import numpy as np


class Landmarks:
    """A class used to reprensent the 21 landmarks of a hand returned by detection_utils.get_landmarks(img)"""

    def __init__(self, landmarks_dict):
        """Initialize a Landmarks object.

        Parameters
        ----------
        landmarks_dict -- a dict[int,tuple] mapping keypoints ids (0 to 20) to normalized (x,y) coordinates
            e.g. {0: (0.1251,0.1994), 1: (0.1513,0.9482), ..., 20: (0.8461,0.7138)}
            This dict can be None.
        """

        self.landmarks = landmarks_dict

    def is_not_none(self):
        return self.landmarks != None

    def get_keypoint_x(self, keypoint):
        """Return the x value of the wanted keypoint

        Parameters
        ----------
        keypoint -- an int in [0,20], the keypoint index for which to return x value.
            See https://google.github.io/mediapipe/solutions/hands.html for more details.

        Return
        ------
        x -- the x value associated to the keypoint (return None if self.landmarks is None)"""

        assert keypoint >= 0 and keypoint <= 20

        x = None
        if self.landmarks:
            x = self.landmarks[keypoint][0]
        return x

    def get_keypoint_y(self, keypoint):
        """Return the y value of the wanted keypoint

        Parameters
        ----------
        keypoint -- an int in [0,20], the keypoint index for which to return y value.
            See https://google.github.io/mediapipe/solutions/hands.html for more details.

        Return
        ------
        y -- the y value associated to the keypoint (return None if self.landmarks is None)"""

        assert keypoint >= 0 and keypoint <= 20
        y = None
        if self.landmarks:
            y = self.landmarks[keypoint][1]
        return y

    def get_distance_between(self, keypoint1, keypoint2):
        """Return the distance beteween the 2 given keypoints
        
        Parameters
        ----------
        keypoint1 -- an int in [0,20], the 1st keypoint index
        keypoint2 -- an int in [0,20], the 2nd keypoint index

        Return
        ------
        distance -- a float, the distance between the 2 keypoints
        """
        kp1 = self.landmarks[keypoint1]
        kp2 = self.landmarks[keypoint2]
        return np.sqrt( (kp1[0]-kp2[0])**2 + (kp1[1]-kp2[1])**2 )
        

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
    Code inspired from https://google.github.io/mediapipe/solutions/hands
    """

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
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
