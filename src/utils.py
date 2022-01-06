import time

import cv2
from numpy import floor

from etc.constants import FRAME_NAME, FONT, FONT_LARGE, CAMERA_FONT_SIZE_MULTIPLIER, CAMERA_FONT_STROKE_MULTIPLIER
from src.CustomExceptions import GameInterruptedException
from src.Landmarks import Landmarks


def display_non_blocking_message(frame, message, font=FONT_LARGE, font_color=(0, 0, 0),
                                 position=(0, 0)):
    #font = _compute_optimal_font(frame.shape[1])
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
            raise RuntimeError("Erreur lecture vidéo pendant affichage message")

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


def get_number_stretched_fingers(landmarks: Landmarks):
    """
    Return the number of stretched fingers corresponding to the numbers of rounds.

    The hand has to be correctly oriented (top of fingers towards the
    top of the image from woth the landmarks has been extracted).
    Works if it's either the hand palm facing the camera or the back of the hand.

    If the landmarks object attribute containing the keypoints is None,
    (i.e. no hand detected) the function returns None.

    Parameters
    ----------
    landmarks -- The landmarks object of the hand for which we want to count the fingers

    Return
    ------
    an int -- the number of stretched fingers (in [0,5])
    """
    if not landmarks.is_not_none():
        return None

    # Determine if it's the palm or the back that is facing the camera
    # in order to choose the condition determining if the thumb is stretched or not
    palm_facing_camera = landmarks.get_keypoint_x(5) < landmarks.get_keypoint_x(17)
    if palm_facing_camera:
        thumb_up = landmarks.get_keypoint_x(4) < landmarks.get_keypoint_x(2)
    else:
        thumb_up = landmarks.get_keypoint_x(4) > landmarks.get_keypoint_x(2)

    index_up = landmarks.get_distance_between(0, 8) > landmarks.get_distance_between(0, 6)
    middle_up = landmarks.get_distance_between(0, 12) > landmarks.get_distance_between(0, 10)
    ring_up = landmarks.get_distance_between(0, 16) > landmarks.get_distance_between(0, 14)
    pinky_up = landmarks.get_distance_between(0, 20) > landmarks.get_distance_between(0, 18)
    return int(thumb_up) + int(index_up) + int(middle_up) + int(ring_up) + int(pinky_up)

def _compute_optimal_font(frame_width):
    font_size = frame_width * CAMERA_FONT_SIZE_MULTIPLIER  
    font_stroke = int(floor(CAMERA_FONT_STROKE_MULTIPLIER[0]*font_size + CAMERA_FONT_STROKE_MULTIPLIER[1]))
    font = (font_size, font_stroke)
    return font