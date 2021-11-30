import cv2
import numpy as np
from settings import settings

def draw_square(img):
    """
    Dessine un carré blanc sur l'image img délimitant
    la zone de détection (carré centré correspondant 
    à la zone renvoyé par crop_image)
    Retourne les coins inférieur gauche et droit du carré
    """
    n,p,_ = img.shape
    t = settings["square_threshold"]
    if n < p :
        start_point = (t, p//2-n//2)
        end_point = (n-t, p//2+n//2)
        bottom_left = (n-t, p//2-n//2)
        bottom_right = (n-t, p//2+n//2)
    elif p < n :
        start_point = (n//2 - p//2, t)
        end_point = (n//2 + p//2, p-t)
        bottom_left = (n//2-p//2, p-t)
        bottom_right = (n//2+p//2, p-t)
    
    img_out = cv2.rectangle(img, start_point[::-1], end_point[::-1], settings["square_color"], settings["square_thickness"])
    return img_out, bottom_left, bottom_right

def crop_image(img):
    """
    Rogne l'image en carré puis recadre l'image img à la taille 48px * 48px
    """
    
    img_out = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    n,p = img_out.shape
    
    # Recadrer l'image en forme carrée au centre
    # Selon le format paysage / portait de l'image
    if n < p :
        img_out = img_out[:, p//2-n//2:p//2+n//2]
    elif p < n :
        img_out = img_out[n//2-p//2:n//2+p//2, :]
        
    # Recadrer l'image en taille 48*48
    width = 48
    height = 48
    dsize = (width, height)
    img_out = cv2.resize(img_out, dsize)
    
    return img_out

def write_expression_on_image(corner, img, expression):
    """
    Écrit sur l'image img le texte "expression".
    """
    n, p, _ = img.shape
    position = (corner[1]+5,corner[0]-10)
    cv2.putText(img, expression, position, settings["font"], 
                                           settings["font_size"],
                                           settings["font_color"][expression][::-1], 
                                           settings["font_stroke"])
    return img

def integrate_small_image(big_image, small_image, br):
    to_integrate = np.zeros((48,48,3))

    to_integrate[:,:,0] = small_image
    to_integrate[:,:,1] = small_image
    to_integrate[:,:,2] = small_image
    
    br2 = (br[0]-settings["square_threshold"], br[1]-settings["square_threshold"])
    big_image[br2[0]-48:br2[0],br2[1]-48:br2[1]] = to_integrate
    
    return big_image

def predict_expression(img, model):
    """
    Predit l'expression de l'image img (48*48 en nuances de gris)
    selon le modèle model spécifié

    Return le label correspondant à la prédiction
    """
    X = img.reshape((48,48,1))
    Ypred = model.predict(np.array([X]))
    emotion_idx = np.argmax(Ypred)
    return settings["labels"][emotion_idx]