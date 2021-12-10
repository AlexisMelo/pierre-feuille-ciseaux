import cv2
import numpy as np
import image_utils as iu
import detection_utils as du
from constants import *


def run_app():
    # define a video capture object (0 = default webcam)
    vid = cv2.VideoCapture(0)

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read(0)

        # Faire le traitement et les modifications d'images ici
        # e.g. : frame = iu.write_score(frame)

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
