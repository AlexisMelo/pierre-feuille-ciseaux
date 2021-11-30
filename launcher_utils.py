import cv2
import numpy as np
import image_utils as img_utils
import tensorflow as tf
from tensorflow import keras
from settings import settings

def lauch_app():
    model = initialize_app()
    run_app(model)

def initialize_app():
    model = keras.models.load_model(settings["path_to_model"])
    return model

def run_app(model):
    # define a video capture object
    vid = cv2.VideoCapture(0)

    detection_enabled = False
    cadre_enabled = True
    small_image_enabled = False

    while(True):
        # Capture the video frame by frame
        ret, frame = vid.read()

        # Processing image
        frame_48_48 = img_utils.crop_image(frame)

        if cadre_enabled:
            frame, corner_bottom_left, corner_bottom_right = img_utils.draw_square(frame)
        
        if detection_enabled:
            frame = img_utils.write_expression_on_image(corner_bottom_left, frame, img_utils.predict_expression(frame_48_48, model))

        if small_image_enabled:
            frame = img_utils.integrate_small_image(frame, frame_48_48, corner_bottom_right)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # Press 'q' to quit
        # Press 'd' to enable/disable the facial expression recognition
        # Press 'c' to enable/disable the limits of the zone
        # Press 'i' to enable/disable the display of the 48*48 image
        key = cv2.pollKey() & 0xFF
        if key == ord('q'):
            break
        elif key == ord('d'):
            detection_enabled = not detection_enabled
        elif key == ord('c'):
            cadre_enabled = not cadre_enabled
        elif key == ord('i'):
            small_image_enabled = not small_image_enabled

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
