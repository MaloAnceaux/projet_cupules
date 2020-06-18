#GUI
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import ctypes

#Text recognition
import pytesseract
from PIL import Image, ImageTk

#path of pytesseract : change it following your installed path
#protocole d'installation :
#   - installer pytesseract grace a l'executable du dossier pytesseract
#   - copier le chemin d'acces de l'executable tesseract.exe ainsi cree et le coller ci-dessous
#   - proceder a l'installation du module 'pip install pytesseract'
#   - importer le module en haut de code 'import pytesseract'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Open cv
import cv2

#Others
import numpy as np
import random as rd
import sys
import matplotlib.pyplot as plt
import copy
import os

#Functions
from threshold import img_threshold
from threshold import find_threshold
from canny_filter import canny_threshold
from canny_filter import enlarge_border
from label import text_recognition
from label import scale
from label import signal
from cupules_detection import detection_cup
#from cupules_detection import discrimination_taille
from cupules_detection import discrimination_surface

#accessing path
path = os.getcwd()+r'\\img_png\\TSC_3_07.png'

#os.chdir(os.getcwd() + r'\\img_png')
#filename = filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'), ('jpg files','.jpg'), ('bmp files','.bmp'), ('all files','.*')]) 


class cupule:
    def __init__(self, points):
        self.points = points
        self.surface = len(points)

    def isolation(self, img_detec):
        self.imprint = np.zeros(np.shape(img_detec))
        for (i, j) in self.points:
            self.imprint[i][j] = 255

try :
#here goes the main code

    img_tot = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img_tot is None : raise ValueError
    
    img = img_tot[0:688]
    img_bandeau = img_tot[688:]
    
    #Scale recognition
    txt_scale = text_recognition(img_bandeau, 419, 652, 43, 80)
    scale_valor = scale(txt_scale, len(img[0]))
    #Signal recognition
    txt_signal = text_recognition(img_bandeau, 656, 870, 39, 71)
    signal_type = signal(txt_signal)

    th = find_threshold(img)

    img_clean = img_threshold(img, th, 8)
    img_canny = enlarge_border(canny_threshold(img_clean, 50, 100))
    img_detec = copy.deepcopy(img_canny)
    
    L = detection_cup(img_detec)
    sorted_L = discrimination_surface(copy.deepcopy(L), img_detec)
    class_cup = [cupule(points) for points in sorted_L]
     
    #im2,contours,hierarchy = cv2.findContours(new_im, 1, 2)
    #cnt = contours[0]
    #perimeter = cv2.arcLength(cnt,True)
    #print(perimeter)
    
    
    #affichage dans la fenetre
    #cv2.imshow("img", img)
    #cv2.imshow("img canny", img_canny)
    #cv2.imshow("img clean", img_clean)
    cv2.imshow("img detec", img_detec)

    cv2.waitKey(0)

except ValueError as er :
    print(f"no image corresponding to path {path}")