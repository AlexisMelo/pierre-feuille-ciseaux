import cv2
import numpy as np
from Memory import Memory
import image_utils as iu
import detection_utils as du
from constants import *
import mediapipe as mp


def run_app_gesture():
    # define a video capture object (0 = default webcam)
    vid = cv2.VideoCapture(0)
    im = Memory(memory_size=10)
    draw = False
    i = 0
    j = 0

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read(0)
        # Flip the image horizontally for a selfie-view display.
        frame = cv2.flip(frame, 1)

        # Faire le traitement et les modifications d'images ici
        frame, landmarks = du.get_landmarks(frame, draw)
        im.add(landmarks)
        gesture = du.get_starting_gesture(im)
        if gesture == LAUNCH_GAME:
            i += 1
            print("LAUNCH ", i)
        elif gesture == STATISTICS:
            j += 1
            print("STATISTICS ", j)

        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (0, 70)
        cv2.putText(
            frame,  # numpy array on which text is written
            str(gesture),  # text
            position,  # position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX,  # font family
            3,  # font size
            (255, 255, 255, 255),  # font color
            3,
        )  # font stroke

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # Press 'q' to quit
        key = cv2.pollKey() & 0xFF
        if key == ord("d"):
            draw = not draw
        if key == ord("q"):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def run_app_count_fingers():
    # define a video capture object (0 = default webcam)
    vid = cv2.VideoCapture(0)
    draw = False

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read(0)
        # Flip the image horizontally for a selfie-view display.
        frame = cv2.flip(frame, 1)

        # Faire le traitement et les modifications d'images ici
        # Landmarks' keypoints coordinates (0,0) is top left, (1,1) is bottom right
        frame, landmarks = du.get_landmarks(frame, draw)
        rounds = du.get_number_of_rounds_posture(landmarks)
        if rounds is not None:
            # print(rounds)
            font = cv2.FONT_HERSHEY_SIMPLEX
            position = (0, 70)
            cv2.putText(
                frame,  # numpy array on which text is written
                str(rounds),  # text
                position,  # position at which writing has to start
                cv2.FONT_HERSHEY_SIMPLEX,  # font family
                3,  # font size
                (255, 255, 255, 255),  # font color
                3,
            )  # font stroke

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # Press 'q' to quit
        key = cv2.pollKey() & 0xFF
        if key == ord("d"):
            draw = not draw
        if key == ord("q"):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Choisissez le mode de fonctionnement :")
    print("1 : Détection de gestes")
    print("2 : Comptage des doigts")
    print()

    mode = int(input())
    if mode == 1:
        run_app_gesture()
    else:
        run_app_count_fingers()
