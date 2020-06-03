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
from circles_detection import hough_circles
from canny_filter import canny_threshold

#chemin d'acces et ouverture avec les trois channels de couleurs
path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\NT_2_03.png'
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

img_clean = seuillage(img, 170, 2)
img_canny = canny_threshold(img_clean, 50, 100)
#img_circles = hough_circles(img_canny, param1=100, param2=30, minRadius=0, maxRadius=300)

#affichage dans la fenetre
cv2.imshow("img canny", img_canny)
#cv2.imshow("img clean", img_circles)


cv2.waitKey(0)