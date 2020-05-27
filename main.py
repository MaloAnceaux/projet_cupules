from PIL import Image, ImageEnhance, ImageFilter

#Text recognition
import pytesseract
import pyocr
import pyocr.builders

#Open cv
import cv2

#Others
import numpy as np
import sys
import matplotlib.pyplot as plt
import copy

from threshold import seuillage
from circles_detection import circle_opencv

#chemin d'acces et ouverture avec les trois channels de couleurs
path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\3_TCS_AMB_2_m-s_20.png'
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

img_clean = seuillage(img, 150, 2)
img_circles = circle_opencv(img_clean, param1=50, param2=25, minRadius=1, maxRadius=300)

#affichage dans la fenetre
cv2.imshow("detected circles", img_circles)
cv2.waitKey(0)