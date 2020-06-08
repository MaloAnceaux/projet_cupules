#from PIL import Image, ImageEnhance, ImageFilter

#Text recognition
#import pytesseract
#import pyocr
#import pyocr.builders

#Open cv
import cv2

#Others
import numpy as np
import random as rd
import sys
import matplotlib.pyplot as plt
import copy

from threshold import img_threshold
from threshold import find_threshold
from circles_detection import hough_circles
from canny_filter import canny_threshold
from cupules_detection import detection_cup
#from sanstitre0 import detection_cup


#accessing path
#path = r'C:\Users\Malo Anceaux\Documents\Cours Mines Paristech\1 A\S2\Projet info\projet_cupules\img_png\TSP410.png'
path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\TSP410.png'

try :
#here goes the main code

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None : raise ValueError

    th = find_threshold(img)

    img_clean = img_threshold(img, th, 6)
    img_canny = canny_threshold(img_clean, 50, 100)

    #img_circles = hough_circles(img_canny, param1=100, param2=30, minRadius=0, maxRadius=300)
    img_detec = copy.deepcopy(img_canny)
    L = detection_cup(img_detec)
    #affichage dans la fenetre

    cv2.imshow("img canny", img_canny)
    cv2.imshow("img clean", img_clean)
    cv2.imshow("img detec", img_detec)
    cv2.waitKey(0)


except ValueError as er :
    print(f"no image corresponding to path {path}")