import time

import cv2

from etc.constants import FRAME_NAME, ALIGNMENT_THRESHOLD, FONT, FONT_LARGE
from src.CustomExceptions import GameInterruptedException


def display_non_blocking_message(frame, message, font=FONT_LARGE, font_color=(0, 0, 0),
                                 position=(0, 0)):
    cv2.putText(
        frame,  # numpy array on which text is written
        message,  # text
        position,  # position at which writing has to start
        FONT,  # font family
        font[0],  # font size
        font_color,  # font color
        font[1],  # font stroke
    )


def display_blocking_message_center(video, message, seconds, font=FONT_LARGE,
                                    font_color=(255, 255, 255, 255)):

    timeout = time.time() + seconds # X seconds depuis mtn

    while time.time() < timeout:

        success, frame = video.read(0)

        if not success:
            print("Erreur lecture vidéo pendant affichage message")
            return

        frame = cv2.flip(frame, 1)

        textsize = cv2.getTextSize(message, FONT, font[0], font[1])[0]
        display_non_blocking_message(frame,
                                     message,
                                     position=(
                                         (frame.shape[1] - textsize[0]) // 2, (frame.shape[0] - textsize[1]) // 2),
                                     font=font,
                                     font_color=font_color)

        cv2.imshow(FRAME_NAME, frame)

        key = cv2.pollKey() & 0xFF
        if key == ord("q"):
            raise GameInterruptedException


def display_non_blocking_message_top_left(frame, message, font=FONT_LARGE, font_color=(0, 0, 0)):
    textsize = cv2.getTextSize(message, FONT, font[0], font[1])[0]
    display_non_blocking_message(frame,
                                 message,
                                 position=((frame.shape[1] - textsize[0]) // 2, 75),
                                 font=font,
                                 font_color=font_color)


def display_non_blocking_message_bottom_left(frame, message, font=FONT_LARGE, font_color=(0, 0, 0)):
    textsize = cv2.getTextSize(message, FONT, font[0], font[1])[0]
    display_non_blocking_message(frame,
                                 message,
                                 position=(25, (frame.shape[0] - textsize[1]) - 25),
                                 font=font,
                                 font_color=font_color)


def display_non_blocking_message_top_center(frame, message, font=FONT_LARGE, font_color=(0, 0, 0)):
    textsize = cv2.getTextSize(message, FONT, font[0], font[1])[0]
    display_non_blocking_message(frame,
                                 message,
                                 position=((frame.shape[1] - textsize[0]) // 2, 75),
                                 font=font,
                                 font_color=font_color)


def are_aligned(point1, point2, point3):
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
    return abs(((y1 - y2) * (x1 - x3)) - ((y1 - y3) * (x1 - x2))) < ALIGNMENT_THRESHOLD
