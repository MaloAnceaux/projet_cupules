#GUI
from tkinter import *
#import tkinter.messagebox as messagebox
#import tkinter.filedialog as filedialog
import ctypes

#Text recognition
import pytesseract
from PIL import Image, ImageTk

#path of pytesseract : change it following your installed path
#protocole d'installation :
#   - telecharger le zip de pytesseract a l'adresse suivante https://github.com/UB-Mannheim/tesseract/wiki
#   - installer pytesseract grace a l'executable precedemment telecharge (il est deja dans le dossier tesseract)
#   - copier le chemin d'acces de l'executable tesseract.exe ainsi cree et le coller ci-dessous
#   - proceder a l'installation du module 'pip install pytesseract'
#   - importer le module en haut de code 'import pytesseract'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Open cv $ pip install opencv-python
import cv2

#Others
import numpy as np
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
from cupules_detection import *

###############################################################################
################################################ GUI's code
###############################################################################

global img_th, img_clean, img_canny, img_detec, scale_valor, signal_type, sorted_cupules_objects
img_th, img_clean, img_canny, img_detec, scale_valor, signal_type, sorted_cupules_objects = None, None, None, None, None, None, None

def window(IMG, largeur, hauteur):
    """
    IMG : image a analyser
    largeur : largeur de l'ecran, parametre automatise
    hauteur : hauteur de l'ecran, parametre automatise
    output : fenetre tk avec fonctions principales
    """
    
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
    t = "%.5e"% scale_valor
    canvas_scale.create_text(70, 30, text=f"Echelle :\n {t} m/px", font=('Cambria', 12))
    canvas_scale.create_text(30, 70, text=f"Signal :\n {signal_type}", font=('Cambria', 12))
    
    #Conversion cv2 --> PIL
    im = img_fromCV2_toPIL(True, IMG)
    im.thumbnail((largeur-200, hauteur))
    
    #Regle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
    canvas._photo = photo=ImageTk.PhotoImage(im)
    canvas.create_image(4, 4, anchor=NW, image=photo)
        
    def dsp_img(image):
        """
        image : image a afficher
        output : affichage de l'image dans la fenetre tk
        """
        im = img_fromCV2_toPIL(True, image)
        im.thumbnail((largeur-200, hauteur))
        
        canvas._photo = photo=ImageTk.PhotoImage(im)
        canvas.create_image(4, 4, anchor=NW, image=photo)
        fenetre.update()
        return(None)
    
    def normal_img():
        """
        output : affichage de l'image normale
        """
        dsp_img(IMG)
        return(None)
        
    def threshold_img():
        """
        output : calcul et affichage de l'image seuillee
        """
        global img_th
        img_th = img_threshold(IMG, threshold_choice.get())
        dsp_img(img_th)
        return(None)
        
    def canny_img():
        """
        output : calcul et affichage de l'image canny
        """
        global img_canny
        if img_clean is not None:
            img_canny = enlarge_border(canny_threshold(img_clean, 50, 100))
            dsp_img(img_canny)
        return(None)

    def cleaner():
        """
        output : calcul et affichage de l'image nettoyee des parasites
        """
        global img_clean
        if img_th is not None:
            img_clean = cleaner_threshold(img_th, number_neighbour.get())
            dsp_img(img_clean)
        return(None)
    
    #Creation des differents widgets (bouttons, scaler...)
    normal_img = Button(fenetre, text="Image normale", width=15, command=normal_img)
    normal_img.pack(side=TOP)
    threshold_img = Button(fenetre, text="Image seuillee", width=15, command=threshold_img)
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
        global img_th, img_clean, img_canny, img_detec, sorted_cupules_objects
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
        L = detection_cup(img_detec)
        clean_L = cleaner_cupule(L)
        sorted_cupules_objects = discrimination_surface(copy.deepcopy(clean_L), img_detec)
        for cupule in sorted_cupules_objects:
            cupule.contour = cupule.contours()
            cupule.deq =  cupule.d_eq()
            Gaxe, Paxe = cupule.axes()
            cupule.GA = Gaxe
            cupule.PA = Paxe
            cupule.fermee = cupule.fermeture(0.8)
        dsp_img(img_detec)
        surf = np.array([cupule.surface for cupule in sorted_cupules_objects])
        plt.hist(surf, bins=100, color="red", alpha=0.8)
        plt.title("Histogramme des surfaces")
        plt.ylabel("Fréquences")
        plt.xlabel("Surface en pixels**2")
        plt.show()
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

############################################ Parametre a changer pour l'analyse
#accessing path
path = os.getcwd()+r'\\img_png\\TSC_3_07.png'
###############################################################################

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