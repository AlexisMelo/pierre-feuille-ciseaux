import cv2

from etc.constants import LAUNCH_GAME, STATISTICS, FRAME_NAME
from src.GameHandler import GameHandler
from src.Landmarks import Landmarks, get_landmarks
from src.Memory import Memory
from src.StatisticsHandler import StatisticsHandler
from src.utils import display_blocking_message_center, display_non_blocking_message_top_left


def _is_hand_at_bottom(landmarks: Landmarks):
    if landmarks.is_not_none() and landmarks.get_keypoint_y(0) > 0.6:
        return True
    return False


def _is_hand_at_top(landmarks: Landmarks):
    if landmarks.is_not_none() and landmarks.get_keypoint_y(0) < 0.4:
        return True
    return False


def _is_hand_on_right_side(landmarks: Landmarks):
    if landmarks.is_not_none() and landmarks.get_keypoint_x(0) > 0.6:
        return True
    return False


def _is_hand_on_left_side(landmarks: Landmarks):
    if landmarks.is_not_none() and landmarks.get_keypoint_x(0) < 0.4:
        return True
    return False


class ApplicationHandler:

    def __init__(self):
        self.memory = Memory(memory_size=10)
        self.draw = False

    def run_application(self):
        print("Avant toute chose... tu pourrais m'indiquer ton pseudo bg ?")
        pseudo = input()
        print(f"Ok {pseudo}, c'est parti !")

        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        key = False
        last_gesture = None

        while key != ord("q"):
            success, frame = video.read(0)  # Capture video frame by frame

            if not success:
                print("Problème de lecture vidéo... arrêt du programme")
                break

            frame = cv2.flip(frame, 1)  # Flip the image horizontally for a selfie-view display

            display_non_blocking_message_top_left(frame, "Effectuez un geste de debut de partie")

            frame, landmarks = get_landmarks(frame, self.draw)
            self.memory.add(landmarks)
            gesture = self.get_starting_gesture(self.memory)

            cv2.imshow(FRAME_NAME, frame)

            if gesture and last_gesture != gesture:
                if gesture == LAUNCH_GAME:
                    display_blocking_message_center(video, "Creation d'une nouvelle partie", 25,
                                                    font_color=(0, 0, 255))
                    game_handler = GameHandler(video)
                    game_handler.initialize_game()
                elif gesture == STATISTICS:
                    display_blocking_message_center(video, "Affichage des statistiques", 25, font_color=(0, 0, 255))
                    statistics_handler = StatisticsHandler(video)
                    statistics_handler.show_stats(pseudo)

            last_gesture = gesture

            key = cv2.pollKey() & 0xFF
            if key == ord("d"):
                self.draw = not self.draw

        print("Arrêt de la capture")
        video.release()
        cv2.destroyAllWindows()

    def get_starting_gesture(self, memory: Memory):
        """
        Return the gesture made by the hand on the image
        which is an element of POSSIBLE_GESTURES
        Code obtained from https://google.github.io/mediapipe/solutions/hands
        """
        if not memory:
            return None

        oldest_landmarks = memory.get_oldest_data()
        newest_landmarks = memory.get_newest_data()

        oldest_hand_on_left_side = _is_hand_on_left_side(oldest_landmarks)
        newest_hand_on_right_side = _is_hand_on_right_side(newest_landmarks)

        oldest_hand_at_top = _is_hand_at_top(oldest_landmarks)
        newest_hand_at_bottom = _is_hand_at_bottom(newest_landmarks)

        swipe_left_to_right = oldest_hand_on_left_side and newest_hand_on_right_side
        swipe_top_to_bottom = oldest_hand_at_top and newest_hand_at_bottom

        # If either both or none of the 2 gestures are detected, return None
        if swipe_top_to_bottom == swipe_left_to_right:
            return None

        if swipe_left_to_right:
            return LAUNCH_GAME

        return STATISTICS
