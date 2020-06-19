from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import ctypes
import os
from PIL import Image, ImageTk

import numpy as np
import copy
import cv2

from threshold import img_threshold
from threshold import cleaner_threshold
from threshold import find_threshold
from canny_filter import canny_threshold
from canny_filter import enlarge_border

user32 = ctypes.windll.user32

#Recuperation des dimensions de l'ecran
largeur = user32.GetSystemMetrics(0)
hauteur = user32.GetSystemMetrics(1)

#Fonction utile globalement dans le code : c'est une fonction vide
#permettant d'attribuer aucune commande a un bouton / un clic-souris etc
def nothing():
    pass

def img_fromCV2_toPIL(gray, image):
    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(image)
    return(im)

def window(IMG, largeur, hauteur, current_img = None):
    global img_th, img_clean, img_canny
    #Creation de la fenetre (objet de la classe Tk) et du canevas qui recevra l'image et les boutons
    fenetre = Tk()
    fenetre.state('zoomed')
    fenetre.configure(bg="white")
    fenetre.title("Cupules detector")
    canvas = Canvas(fenetre, bg="white", highlightthickness=4, height=hauteur, width=largeur-200)
    canvas.pack(side=LEFT)
    
    
    #Conversion cv2 --> PIL
    im = img_fromCV2_toPIL(True, IMG)
    im.thumbnail((largeur-200, hauteur))
    
    #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
    canvas._photo = photo=ImageTk.PhotoImage(im)
    canvas.create_image(4, 4, anchor=NW, image=photo)
    
    img_th, img_clean, img_canny = None, None, None
    
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
        global cleaner_img, number_neighbour, img_th, img_clean
        img_th = img_threshold(IMG, threshold_choice.get())
        dsp_img(img_th)
        if img_clean is None:
            cleaner_img = Button(fenetre, text="Nettoyage image", width=15, command=cleaner)
            cleaner_img.pack(side=TOP)
            number_neighbour = Scale(fenetre, orient='horizontal', from_=0, to=12, resolution=1, tickinterval=3, length=150, label='Nombre voisin min')
            number_neighbour.pack(side=TOP)
            img_clean = 1
        return(None)
        
    def canny_img():
        global img_canny
        img_canny = enlarge_border(canny_threshold(img_clean, 50, 100))
        dsp_img(img_canny)
        return(None)

    def cleaner():
        global img_clean, img_th
        img_clean = cleaner_threshold(img_th, number_neighbour.get())
        dsp_img(img_clean)
        img_th = copy.deepcopy(img_clean)
        return(None)
        
    normal_img = Button(fenetre, text="Image normale", width=15, command=normal_img)
    normal_img.pack(side=TOP)        
    threshold_img = Button(fenetre, text="Image seuillée", width=15, command=threshold_img)
    threshold_img.pack(side=TOP)
    canny_img = Button(fenetre, text="Filtre de Canny", width=15, command=canny_img)
    canny_img.pack(side=TOP)
    
    threshold_choice = Scale(fenetre, orient='horizontal', from_=0, to=255, resolution=1, tickinterval=50, length=150, label='Valeur seuillage')
    threshold_choice.pack(side=TOP)
    
    #Lancement de la routine (receptionnaire d'evenements)
    fenetre.mainloop()
    
    return(None)

path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\TSC_3_07.png'

img_tot = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
if img_tot is None : raise ValueError
    
img = img_tot[0:688]
img_bandeau = img_tot[688:]

window(img, largeur, hauteur)