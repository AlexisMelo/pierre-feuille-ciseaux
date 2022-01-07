import cv2

from etc.constants import LAUNCH_GAME, MEMORY_SIZE, STATISTICS, FRAME_NAME, CLOSE, RED, BLUE
from src.GameHandler import GameHandler
from src.CustomExceptions import GameInterruptedException, ApplicationInterruptedException
from src.Landmarks import Landmarks, get_landmarks
from src.Memory import Memory
from src.StatisticsHandler import StatisticsHandler
from src.utils import display_blocking_message_center, display_non_blocking_message_top_center, get_number_stretched_fingers


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

def  _is_hand_open(landmarks: Landmarks):
    if landmarks.is_not_none() and get_number_stretched_fingers(landmarks) == 5:
        return True
    return False

def  _is_hand_closed(landmarks: Landmarks):
    if landmarks.is_not_none() and get_number_stretched_fingers(landmarks) == 0:
        return True
    return False

class ApplicationHandler:

    def __init__(self, statistics_handler):
        self.memory = Memory(memory_size=MEMORY_SIZE)
        self.draw = False
        self.statistics_handler = statistics_handler

    def run_application(self):
        print("Avant toute chose... tu pourrais m'indiquer ton pseudo bg ?")
        pseudo = input()
        print(f"Ok {pseudo}, c'est parti !")

        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        last_gesture = None

        try:
            while True:
                success, frame = video.read(0)  # Capture video frame by frame

                if not success:
                    raise RuntimeError("Problème de lecture vidéo... arrêt du programme")

                frame = cv2.flip(frame, 1)  # Flip the image horizontally for a selfie-view display

                display_non_blocking_message_top_center(frame, "Effectuez un geste de debut de partie")

                frame, landmarks = get_landmarks(frame, self.draw)
                self.memory.add(landmarks)
                gesture = self.get_starting_gesture(self.memory)

                cv2.imshow(FRAME_NAME, frame)

                if gesture and last_gesture != gesture:
                    if gesture == LAUNCH_GAME:
                        display_blocking_message_center(video, "Creation d'une nouvelle partie", seconds=3, font_color=BLUE)
                        game_handler = GameHandler(video, pseudo, self.statistics_handler)
                        game_handler.initialize_game()
                    elif gesture == STATISTICS:
                        display_blocking_message_center(video, "Affichage des statistiques", seconds=3, font_color=BLUE)
                        self.statistics_handler.show_stats(video, pseudo)
                    elif gesture == CLOSE:
                        display_blocking_message_center(video, "Au revoir !", seconds=1, font_color=RED)
                        raise ApplicationInterruptedException

                last_gesture = gesture

                key = cv2.pollKey() & 0xFF
                if key == ord("d"):
                    self.draw = not self.draw
                if key == ord("q"):
                    raise ApplicationInterruptedException
        except ApplicationInterruptedException:
            print("Application interrompue volontairement")
        except GameInterruptedException:
            print("Partie interrompue volontairement")
            self.statistics_handler.increment_global_stats("games_abandoned")
        except Exception as e:
            print(f"Partie interrompue subitement : {e}")

        print("Arrêt de la capture")
        video.release()
        cv2.destroyAllWindows()

    def get_starting_gesture(self, memory: Memory):
        """
        Return the gesture made by the hand on the image
        which is an element of POSSIBLE_GESTURES

        Parameters
        ----------
        memory -- a Memory object, the memory to search in

        Return
        ------
        a string -- The recognized gesture LAUNCH_GAME or STATISTICS, or None if nothing is detected
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

        oldest_hand_open = _is_hand_open(oldest_landmarks)
        newest_hand_closed = _is_hand_closed(newest_landmarks)

        if oldest_hand_open and newest_hand_closed:
            return CLOSE

        # If either both or none of the 2 gestures are detected, return None
        if swipe_top_to_bottom == swipe_left_to_right:
            return None

        if swipe_left_to_right:
            return LAUNCH_GAME
        
        return STATISTICS

