import cv2
import numpy as np
from etc.constants import *


def display_computer_game_posture(img, posture_computer):
    if posture_computer == PIERRE:
        url = "pierre.png"
    elif posture_computer == FEUILLE:
        url = "feuille.png"
    else:
        url = "ciseaux.png"
    # Read logo and resize
    image_to_display = cv2.imread(url)
    size = 100
    image_to_display = cv2.resize(image_to_display, (size, size))
    # Create a mask of logo
    img2gray = cv2.cvtColor(image_to_display, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
    # Region of Image (ROI), where we want to insert logo
    roi = img[-size-370:-370, -size-70:-70]
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += image_to_display
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'GESTURE OF COMPUTER :', (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    return img


def display_winner_or_round(img, winner):
    if winner == COMPUTER_WIN: 
        msg = "COMPUTER WIN"
        width = 220
    else: 
        msg = "PLAYER WIN"
        width = 250
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, msg, (width, 450), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    return img


def display_final_winner(img, winner, score):
    if winner == COMPUTER_WIN: 
        msg = "COMPUTER WIN THE GAME" + score
        width = 80
    else: 
        msg = "PLAYER WIN THE GAME" + score
        width = 110
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, msg, (width, 450), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    return img


def display_scores_previous_games(img, scores):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "PREVIOUS SCORES :", (300, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    height = 90
    for score in scores:
        cv2.putText(img, score, (550, height), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        height  += 50
    return img
