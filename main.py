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
from threshold import cleaner_threshold

from canny_filter import canny_threshold
from canny_filter import enlarge_border

from label import text_recognition
from label import scale
from label import signal

import cupules_detection as cup


###############################################################################
################################################ Class Cupule
###############################################################################

class Cupule:
    def __init__(self, points, img, border):
        self.points = points
        self.surface = len(points)
        self.imprint = self.isolation(img)
        self.border = border  #True si cupule en bordure d'image

    def isolation(self, img):
        imprint = np.zeros(np.shape(img))
        for (i, j) in self.points:
            imprint[i][j] = 255
        return imprint

###############################################################################
################################################ GUI's code
###############################################################################

global img_th, img_clean, img_canny, img_detec, scale_valor, signal_type
img_th, img_clean, img_canny, img_detec, scale_valor, signal_type = None, None, None, None, None, None

def window(IMG, largeur, hauteur, current_img = None):
    
    def nothing():
        pass
    
    def img_fromCV2_toPIL(gray, image):
        if gray:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image)
        return(im)
    
    #Creation de la fenetre (objet de la classe Tk) et du canevas qui recevra l'image et les boutons
    fenetre = Tk()
    fenetre.state('zoomed')
    fenetre.configure(bg="white")
    fenetre.title("Cupules detector")
    canvas = Canvas(fenetre, bg="white", highlightthickness=4, height=hauteur, width=largeur-200)
    canvas.pack(side=LEFT)
    
    canvas_scale = Canvas(fenetre, bg="white", height=100, width=200)
    canvas_scale.pack(side=BOTTOM)
    canvas_scale.create_text(95, 30, text=f"Échelle :\n {scale_valor} m/px", font=('Cambria', 12))
    canvas_scale.create_text(30, 70, text=f"Signal :\n {signal_type}", font=('Cambria', 12))

    
    #Conversion cv2 --> PIL
    im = img_fromCV2_toPIL(True, IMG)
    im.thumbnail((largeur-200, hauteur))
    
    #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
    canvas._photo = photo=ImageTk.PhotoImage(im)
    canvas.create_image(4, 4, anchor=NW, image=photo)
        
    def dsp_img(image):
        im = img_fromCV2_toPIL(True, image)
        im.thumbnail((largeur-200, hauteur))
        
        canvas._photo = photo=ImageTk.PhotoImage(im)
        canvas.create_image(4, 4, anchor=NW, image=photo)
        fenetre.update()
        return(None)
    
    def normal_img():
        dsp_img(IMG)
        return(None)
        
    def threshold_img():
        global img_th
        img_th = img_threshold(IMG, threshold_choice.get())
        dsp_img(img_th)
        return(None)
        
    def canny_img():
        global img_canny
        if img_clean is not None:
            img_canny = enlarge_border(canny_threshold(img_clean, 50, 100))
            dsp_img(img_canny)
        return(None)

    def cleaner():
        global img_clean
        if img_th is not None:
            img_clean = cleaner_threshold(img_th, number_neighbour.get())
            dsp_img(img_clean)
        return(None)
        
    normal_img = Button(fenetre, text="Image normale", width=15, command=normal_img)
    normal_img.pack(side=TOP)        
    threshold_img = Button(fenetre, text="Image seuillée", width=15, command=threshold_img)
    threshold_img.pack(side=TOP)
    canny_img = Button(fenetre, text="Filtre de Canny", width=15, command=canny_img)
    canny_img.pack(side=TOP)    
    threshold_choice = Scale(fenetre, orient='horizontal', from_=0, to=255, resolution=1, tickinterval=50, length=150, label='Valeur seuillage')
    threshold_choice.pack(side=TOP)
    cleaner_img = Button(fenetre, text="Nettoyage image", width=15, command=cleaner)
    cleaner_img.pack(side=TOP)
    number_neighbour = Scale(fenetre, orient='horizontal', from_=0, to=16, resolution=1, tickinterval=5, length=150, label='Nombre voisin min')
    number_neighbour.pack(side=TOP)
    
    def detection():
        global img_th, img_clean, img_canny, img_detec
        if img_th is None:
            img_th = img_threshold(IMG, threshold_choice.get())
        if img_clean is None:
            img_clean = cleaner_threshold(img_th, number_neighbour.get())
        if img_canny is None:
            img_canny = enlarge_border(canny_threshold(img_clean, 50, 100))
        normal_img['state'] = DISABLED
        threshold_img['state'] = DISABLED
        canny_img['state'] = DISABLED
        cleaner_img['state'] = DISABLED
        
        img_detec = copy.deepcopy(img_canny)
        dsp_img(img_detec)
        L = cup.detection_cup(img_detec)
        clean_L = cup.cleaner_cupule(L)
        sorted_L = cup.discrimination_surface(copy.deepcopy(clean_L), img_detec)
        class_cup = [cupule(points) for points in sorted_L]
        return(None)
    
    start_analysis = Button(fenetre, text="Lancer l'analyse", width=15, command=detection)
    start_analysis.pack(side=BOTTOM)
    
    #Lancement de la routine (receptionnaire d'evenements)
    fenetre.mainloop()
    
    return(None)

###############################################################################
################################################ Main code
###############################################################################

#os.chdir(str(os.getcwd() + r'\\img_png'))
#path = filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'), ('jpg files','.jpg'), ('bmp files','.bmp'), ('all files','.*')])

#accessing path
path = os.getcwd()+r'\\img_png\\TSC_3_07.png'

img_tot = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
img = img_tot[0:688]
img_bandeau = img_tot[688:]

#Scale recognition
txt_scale = text_recognition(img_bandeau, 419, 652, 43, 80)
scale_valor = scale(txt_scale, len(img[0]))
#Signal recognition
txt_signal = text_recognition(img_bandeau, 656, 870, 39, 71)
signal_type = signal(txt_signal)

user32 = ctypes.windll.user32
#Recuperation des dimensions de l'ecran
largeur = user32.GetSystemMetrics(0)
hauteur = user32.GetSystemMetrics(1)

window(img, largeur, hauteur)