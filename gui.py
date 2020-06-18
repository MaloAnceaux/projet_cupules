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

def window(IMG, largeur, hauteur):       
    #Creation de la fenetre (objet de la classe Tk) et du canevas qui recevra l'image et les boutons
    fenetre = Tk()
    fenetre.state('zoomed')
    fenetre.configure(bg="white")
    fenetre.title("Cupules detector")
    canvas = Canvas(fenetre, bg="white", highlightthickness=4, height=hauteur, width=largeur-200)
    canvas.pack(side=LEFT)
    
    #Conversion cv2 --> PIL
    #im = img_fromCV2_toPIL(True, IMG)
    #im.thumbnail((largeur-200, hauteur))
    
    #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
    #photo = ImageTk.PhotoImage(im)
    #canvas.create_image(4, 4, anchor=NW, image=photo)
    
    def dsp_img():
        canvas.delete(all)
        
        #Conversion cv2 --> PIL
        im = img_fromCV2_toPIL(True, IMG)
        im.thumbnail((largeur-200, hauteur))
        
        #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
        photo = ImageTk.PhotoImage(im)
        canvas.create_image(4, 4, anchor=NW, image=photo)
    
    def dsp_threshold_img():
        img_clean = img_threshold(IMG,threshold_choice.get(),number_neighbour.get())
        
        canvas.delete(all)
        
        #Conversion cv2 --> PIL
        im = img_fromCV2_toPIL(True, img_clean)
        im.thumbnail((largeur-200, hauteur))
        
        #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
        photo = ImageTk.PhotoImage(im)
        canvas.create_image(4, 4, anchor=NW, image=photo)
        
    def dsp_canny_img():
        img_canny = 
        
        canvas.delete(all)
        
        #Conversion cv2 --> PIL
        im = img_fromCV2_toPIL(True, IMG)
        im.thumbnail((largeur-200, hauteur))
        
        #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
        photo = ImageTk.PhotoImage(im)
        canvas.create_image(4, 4, anchor=NW, image=photo)
    
        
    normal_img = Button(fenetre, text="Image normale", width=15, command=dsp_img)
    normal_img.pack(side=TOP)        
    threshold_img = Button(fenetre, text="Image seuillée", width=15, command=dsp_threshold_img)
    threshold_img.pack(side=TOP)
    canny_img = Button(fenetre, text="Filtre de Canny", width=15, command=dsp_canny_img)
    canny_img.pack(side=TOP)
        
        
    threshold_button = Button(fenetre, text="Seuillage", width=10, command=seuillage)
    threshold_button.pack(side=TOP)
    
    threshold_choice = Scale(fenetre, orient='horizontal', from_=0, to=255, resolution=1, tickinterval=50, length=150, label='Valeur seuillage')
    threshold_choice.pack(side=TOP)
    number_neighbour = Scale(fenetre, orient='horizontal', from_=0, to=12, resolution=1, tickinterval=3, length=150, label='Nombre voisin min')
    number_neighbour.pack(side=TOP)
   
    
    #check1 = BooleanVar()
    #Cette instruction instancie un objet de la classe BooleanVar(),
    #laquelle fait partie du module Tkinter au meme titre que les
    #classes similaires DoubleVar(), StringVar() et IntVar()
    #Toutes ces classes permettent de definir des « variables Tkinter »,
    #lesquelles sont en fait des objets, mais qui se se comportent
    #comme des variables a l'interieur des widgets Tkinter
    #Ainsi, check sera une variable qui pourra adopter comme valeur True ou False
    
    #CheckDaltonisme = Checkbutton(fenetre_initiale, text= "Etes-vous daltonien(s) ?", variable=check1, command=CheckDaltonisme)
    #CheckDaltonisme.pack(pady=5)
    #Creation d'une case a cocher, contenant la variable Booleenne check (cf ci-dessus)
    #et activant la fonction CheckDaltonisme lorsque la case change d'etat (cochee --> decochee ou inverse)

    fenetre.mainloop()
    #Lancement de la routine (receptionnaire d'evenements)
    
    return(None)

path = r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\TSC_3_07.png'

img_tot = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
if img_tot is None : raise ValueError
    
img = img_tot[0:688]
img_bandeau = img_tot[688:]

window(img, largeur, hauteur)