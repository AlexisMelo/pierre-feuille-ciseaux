from constants import *
from detection_utils import get_landmarks


class ImageMemory:
    """A class used to store previous images in order to recognize gestures"""

    def __init__(self, memory_size=MEMORY_SIZE):
        assert memory_size > 0
        self.memory = []
        self.memory_size = memory_size

    def add(self, img):
        # If the memory is full, delete the oldest image
        if len(self.memory) >= self.memory_size:
            _ = self.memory.pop(0)
        self.memory.append(img)

    def _get_oldest_image(self):
        """Return the oldest image stored in memory if exists"""
        if len(self.memory) != 0:
            return self.memory[0]
        else:
            return None

    def _get_newest_image(self):
        """Return the newest image stored in memory is exists"""
        if len(self.memory) != 0:
            return self.memory[-1]
        else:
            return None

    def recognize_start_gesture(self):
        oldest_img = self._get_oldest_image()
        newest_img = self._get_newest_image()
        _, oldest_landmarks = get_landmarks(oldest_img)
        _, newest_landmarks = get_landmarks(newest_img)

        oldest_hand_on_left_side = self._is_hand_on_left_side(oldest_landmarks)
        newest_hand_on_right_side = self._is_hand_on_right_side(newest_landmarks)

        if oldest_hand_on_left_side and newest_hand_on_right_side:
            return LAUNCH_GAME
        else:
            return None

    def _is_hand_on_left_side(self, landmarks):
        if landmarks and landmarks[4][0] > 0.6:
            return True
        return False

    def _is_hand_on_right_side(self, landmarks):
        if landmarks and landmarks[4][0] < 0.4:
            return True
        return False
