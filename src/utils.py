import cv2
import numpy as np

from etc.constants import FRAME_NAME, ALIGNMENT_THRESHOLD 
from src.GameInterruptedException import GameInterruptedException

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_STROKE = 5


def display_blocking_message_center(video, message, number_of_frames, font_size=2,
                                    font_color=(255, 255, 255, 255),
                                    font_stroke=FONT_STROKE):
    number_of_frames_shown = 0

    while number_of_frames_shown < number_of_frames:

        success, frame = video.read(0)

        if not success:
            print("Erreur lecture vidéo pendant affichage message")
            return

        frame = cv2.flip(frame, 1)

        textsize = cv2.getTextSize(message, FONT, font_size, font_stroke)[0]
        cv2.putText(
            frame,  # numpy array on which text is written
            message,  # text
            (
                (frame.shape[1] - textsize[0]) // 2,
                (frame.shape[0] - textsize[1]) // 2,
            ),  # position at which writing has to start
            FONT,  # font family
            font_size,  # font size
            font_color,  # font color
            font_stroke,  # font stroke
        )

        cv2.imshow(FRAME_NAME, frame)

        number_of_frames_shown = number_of_frames_shown + 1

        key = cv2.pollKey() & 0xFF
        if key == ord("q"):
            raise GameInterruptedException


def display_non_blocking_message_top_left(frame, message, font_size=2, font_color=(0, 0, 0)):
    textsize = cv2.getTextSize(message, FONT, font_size, FONT_STROKE)[0]

    cv2.putText(
        frame,  # numpy array on which text is written
        message,  # text
        (
            (frame.shape[1] - textsize[0]) // 2,
            75
        ),  # position at which writing has to start
        FONT,  # font family
        font_size,  # font size
        font_color,  # font color
        FONT_STROKE,  # font stroke
    )


def display_non_blocking_message_bottom_left(frame, message, font_size=2, font_color=(0, 0, 0)):
    textsize = cv2.getTextSize(message, FONT, font_size, FONT_STROKE)[0]

    cv2.putText(
        frame,  # numpy array on which text is written
        message,  # text
        (
            25,
            (frame.shape[0] - textsize[1]) - 25
        ),  # position at which writing has to start
        FONT,  # font family
        font_size,  # font size
        font_color,  # font color
        FONT_STROKE,  # font stroke
    )


def are_aligned(point1, point2, point3) :
    """Determine is the 3 given points are aligned
    
    Parameters
    ----------
    point1, point2, point3 : float tuples under (x,y) format

    Return
    ------
    a boolean -- True if the points are aligned at tolerance ALIGNMENT_THRESHOLD
    """
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return np.abs(((y1-y2)*(x1-x3)) - ((y1-y3)*(x1-x2))) < ALIGNMENT_THRESHOLD