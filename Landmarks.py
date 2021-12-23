from constants import *


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
