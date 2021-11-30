import cv2

settings = {
    ### MODEL ###
    "path_to_model" : "./model300",

    ### LABELS ###
    "labels" : {0:"Angry", 1:"Disgust", 2:"Fear", 3:"Happy", 4:"Sad", 5:"Surprise", 6:"Neutral"},

    ### FONT ###
    "font" : cv2.FONT_HERSHEY_SIMPLEX,
    "font_size" : 2,
    "font_color" : {"Neutral":(255,255,255), "Angry":(255,0,0), "Happy":(255,211,25), "Sad":(0,96,255), "Disgust":(0,255,0), "Fear":(153,90,233), "Surprise":(230,0,126)}, #RGB Format
    "font_stroke" : 7,

    ### SQUARE ###
    "square_color" : (255, 255, 255),
    "square_thickness" : 6,
    "square_threshold" : 5 
}