from PIL import Image, ImageTk
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import ctypes
import os

import cv2
user32 = ctypes.windll.user32

largeur = user32.GetSystemMetrics(0)
hauteur = user32.GetSystemMetrics(1)
#Indice de proportionnalite de hauteur
#hauteur ecran / hauteur canevas principal (le plus grand donc de reference)
#et -30 pour laisser une "marge de securite"

#Fonction utile globalement dans le code : c'est une fonction vide
#permettant d'attribuer aucune commande a un bouton / un clic-souris etc
def nothing():
    pass

def window(img, largeur, hauteur):
    global fenetre_initiale, BoutonSingleplayer, BoutonMultiplayer, CheckDaltonisme, check1
    
    fenetre = Tk()
    fenetre.configure(bg="white")
    fenetre.title("Cupules detector")
    canvas = Canvas(fenetre, bg="white", highlightthickness=4, height=hauteur, width=largeur)
    canvas.pack()
    #Creation de la fenetre (objet de la classe Tk) et du canevas qui recevra l'image et les boutons
        
    im = Image.fromarray(img)
    im = im.resize((largeur, hauteur), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image = im)

    canvas.create_image(0, 0, anchor = NW, image = photo)
    #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
    
    def seuillage():
        pass
    
    start_button = Button(fenetre, text="Démarrer la procédure", width=15, command=seuillage)
    start_button.pack()
   
    
    check1 = BooleanVar()
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

window(img_tot, largeur, hauteur)