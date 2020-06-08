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

#Functions
from threshold import img_threshold
from threshold import find_threshold
from canny_filter import canny_threshold
from canny_filter import enlarge_border
from cupules_detection import detection_cup

#accessing path
#path = r'C:\Users\Malo Anceaux\Documents\Cours Mines Paristech\1 A\S2\Projet info\projet_cupules\img_png\TSP410.png'
path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\TSP410.png'

try :
#here goes the main code

    img_tot = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img_tot is None : raise ValueError
    
    img = img_tot[0:688]
    img_bandeau = img_tot[688:]

    th = find_threshold(img)

    img_clean = img_threshold(img, th, 6)
    img_canny = canny_threshold(img_clean, 50, 100)
    img_canny = enlarge_border(img_canny)

    img_detec = copy.deepcopy(img_canny)
    L = detection_cup(img_detec)
    #affichage dans la fenetre

    #cv2.imshow("img canny", img_canny)
    #cv2.imshow("img clean", img_clean)
    cv2.imshow("img detec", img_detec)
    cv2.waitKey(0)

except ValueError as er :
    print(f"no image corresponding to path {path}")