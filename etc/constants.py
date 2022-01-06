################
### POSTURES ###
################
import cv2
from numpy import floor

PIERRE = "pierre"
FEUILLE = "feuille"
CISEAUX = "ciseaux"
POSSIBLE_GAME_POSTURES = [PIERRE, FEUILLE, CISEAUX]

# Float between 1 included and +inf
# The bigger it is, the wider the user has to open its 2 fingers (index and middle) in order to be recognized as a CISEAUX
# The closer it gets to 1, the smaller the user has to open its 2 fingers in order to be recognized as a CISEAUX
CISEAUX_THRESHOLD = 2

# Float between 0 included and +inf
# The closer it gets to 1, the more stuck the fingers has to be in order to be recognized has a FEUILLE
# The bigger it gets, the less stuck the fingers has to be in order to be recognized has a FEUILLE
FEUILLE_THRESHOLD = 1.2

# FLoat between 0 and +inf
# The closer it gets to 0, the more aligned the thumb as to be to be considered ad stretched
# The bigger it gets, the less aligned tje thumb as to be to be considered as stretched
ALIGNMENT_THRESHOLD = 0.003

################
### GESTURES ###
################

LAUNCH_GAME = "launch_game"
STATISTICS = "statistics"
POSSIBLE_GESTURES = [LAUNCH_GAME, STATISTICS]
CLOSE = "close"
# Keep the 10 last images data in memory to detect the gestures
MEMORY_SIZE = 10

################
###  WINNER  ###
################

PLAYER_WIN = "Player"
COMPUTER_WIN = "Computer"

################
###   GAME   ###
################
NB_MAX_ROUND = 5
FRAME_NAME = "Pierre feuille ciseaux"

################
###   MESSAGES   ###
################
FONT = cv2.FONT_HERSHEY_SIMPLEX

CAMERA_FONT_SIZE_MULTIPLIER = 1/640
CAMERA_FONT_STROKE_MULTIPLIER = (3, -1)

FONT_SIZE_LARGE = 2  
FONT_STROKE_LARGE = 5
FONT_LARGE = (FONT_SIZE_LARGE, FONT_STROKE_LARGE)

FONT_SIZE_NORMAL = 1.5
FONT_STROKE_NORMAL = 3
FONT_NORMAL = (FONT_SIZE_NORMAL, FONT_STROKE_NORMAL)

FONT_SIZE_SMALL = 1
FONT_STROKE_SMALL = 2
FONT_SMALL = (FONT_SIZE_SMALL, FONT_STROKE_SMALL)

FONT_SIZE_XS = 0.8
FONT_STROKE_XS = 2
FONT_XS = (FONT_SIZE_XS, FONT_STROKE_XS)
