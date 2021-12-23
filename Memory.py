from constants import *


class Memory:
    """A class used to store previous images data in order to recognize gestures"""

    def __init__(self, memory_size=MEMORY_SIZE):
        assert memory_size > 0
        self.memory = []
        self.memory_size = memory_size

    def add(self, data):
        # If the memory is full, delete the oldest data
        if len(self.memory) >= self.memory_size:
            _ = self.memory.pop(0)
        self.memory.append(data)

    def _get_oldest_data(self):
        """Return the oldest data stored in memory if exists"""
        if len(self.memory) != 0:
            return self.memory[0]
        else:
            return None

    def _get_newest_data(self):
        """Return the newest data stored in memory is exists"""
        if len(self.memory) != 0:
            return self.memory[-1]
        else:
            return None

    def recognize_starting_gesture(self):
        oldest_landmarks = self._get_oldest_data()
        newest_landmarks = self._get_newest_data()

        oldest_hand_on_left_side = self._is_hand_on_left_side(oldest_landmarks)
        newest_hand_on_right_side = self._is_hand_on_right_side(newest_landmarks)

        oldest_hand_at_top = self._is_hand_at_top(oldest_landmarks)
        newest_hand_at_bottom = self._is_hand_at_bottom(newest_landmarks)

        swipe_left_to_right = oldest_hand_on_left_side and newest_hand_on_right_side
        swipe_top_to_bottom = oldest_hand_at_top and newest_hand_at_bottom

        # If either both or none of the 2 gestures are detected, return None
        if swipe_top_to_bottom == swipe_left_to_right:
            return None
        else:
            if swipe_left_to_right:
                return LAUNCH_GAME
            else:
                return STATISTICS

    def _is_hand_on_left_side(self, landmarks):
        if landmarks.is_not_none() and landmarks.get_keypoint_x(0) > 0.6:
            return True
        return False

    def _is_hand_on_right_side(self, landmarks):
        if landmarks.is_not_none() and landmarks.get_keypoint_x(0) < 0.4:
            return True
        return False

    def _is_hand_at_top(self, landmarks):
        if landmarks.is_not_none() and landmarks.get_keypoint_y(0) < 0.4:
            return True
        return False

    def _is_hand_at_bottom(self, landmarks):
        if landmarks.is_not_none() and landmarks.get_keypoint_y(0) > 0.6:
            return True
        return False
