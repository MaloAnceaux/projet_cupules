#GUI
from tkinter import *
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

global img_th, img_clean, img_canny, img_detec, img_sorted, img_finale, scale_valor, signal_type, cupules_objects, sorted_cupules_objects, name_img
img_th, img_clean, img_canny, img_detec, img_sorted, img_finale, scale_valor, signal_type, cupules_objects, sorted_cupules_objects, name_img = None, None, None, None, None, None, None, None, None, None, None

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
        """
        output : conversion d'une image opencv en image PIL'
        """
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
    
    #Creation des differents widgets (boutons, scaler...)
    normal_img = Button(fenetre, text="Image normale", width=15, command=normal_img)
    normal_img.pack(side=TOP)
    threshold_choice = Scale(fenetre, orient='horizontal', from_=0, to=255, resolution=1, tickinterval=50, length=150, label='Valeur seuillage')
    threshold_choice.pack(side=TOP)
    threshold_img = Button(fenetre, text="Image seuillee", width=15, command=threshold_img)
    threshold_img.pack(side=TOP)
    number_neighbour = Scale(fenetre, orient='horizontal', from_=0, to=16, resolution=1, tickinterval=5, length=150, label='Nombre voisin min')
    number_neighbour.pack(side=TOP)
    cleaner_img = Button(fenetre, text="Nettoyage image", width=15, command=cleaner)
    cleaner_img.pack(side=TOP)
    canny_img = Button(fenetre, text="Filtre de Canny", width=15, command=canny_img)
    canny_img.pack(side=TOP)
    
    def detection():
        """
        output : detecte les zones noires connexes sur l'image (cupules, vraies et fausses)
        """
        global img_th, img_clean, img_canny, img_detec, cupules_objects
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
        start_detection['state'] = DISABLED
        
        img_detec = copy.deepcopy(img_canny)
        cupules_objects = detection_cup(img_detec)
        surf = np.array([cupule.surface for cupule in cupules_objects])
        
        #Histogramme en echelle lineaire
        plt.subplot(311)
        hist, bins, _  = plt.hist(surf, bins=100, color="red", alpha=0.8)
        plt.title("Histogramme des surfaces")
        plt.ylabel("Frequences")
        plt.xlabel("Surface en pixels**2")
        
        #Histogramme en echelle logarithmique 
        logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        plt.subplot(313)
        plt.hist(surf, bins=logbins, color="red", alpha=0.8)
        plt.title("Histogramme des surfaces (echelle log)")
        plt.ylabel("Frequences")
        plt.xlabel("Surface en pixels**2")
        plt.xscale('log')
        plt.show()
        return(None)
    
    #Autres widgets
    start_detection = Button(fenetre, text="Lancer la detection", width=15, command=detection)
    start_detection.pack(side=TOP)
    percentage_surface_min = Scale(fenetre, orient='horizontal', from_=0, to=90, resolution=2, tickinterval=20, length=150, label='Pourcentage surface min')
    percentage_surface_min.pack(side=TOP)
    percentage_surface_max = Scale(fenetre, orient='horizontal', from_=0, to=10, resolution=0.01, tickinterval=5, length=150, label='Pourcentage surface max')
    percentage_surface_max.pack(side=TOP)
    critere_surface = Scale(fenetre, orient='horizontal', from_=0, to=10, resolution=0.5, tickinterval=2, length=150, label='Critere surface')
    critere_surface.pack(side=TOP)
    
    def refresh():
        """
        output : affichage de l'image finalement traitable
        """
        global sorted_cupules_objects, img_sorted, img_finale
        if cupules_objects is None:
            detection()
        
        sorted_cupules_objects, img_sorted, img_finale = refresh_affichage_cupules(cupules_objects, img_detec, percentage_surface_max.get(), percentage_surface_min.get(), critere_surface.get())
        dsp_img(img_sorted)
        return(None)
    
    start_refresh = Button(fenetre, text="Discrimination surface", width=17, command=refresh)
    start_refresh.pack(side=TOP)
    
    def analysis():
        """
        output : analyse finale des cupules gardees dans le calcul, affichage et enregistrement des graphes correspondant a l'analyse et enregistrement des resultats en format txt
        """
        if sorted_cupules_objects is None:
            refresh()
        start_analysis['state'] = DISABLED
        
        #Calcul des differents parametres caracterisant chaque cupule
        for cupule in sorted_cupules_objects:
            cupule.contour = cupule.contours()
            cupule.deq =  cupule.d_eq()
            Gaxe, Paxe = cupule.axes()
            cupule.GA = Gaxe
            cupule.PA = Paxe
            cupule.fermee = cupule.fermeture(0.8)
        
        #Affichage des graphes
        surf = np.array([cupule.surface*scale_valor**2 for cupule in sorted_cupules_objects])
        enclosure = np.array([cupule.fermee for cupule in sorted_cupules_objects])
        index_enclosure = np.where(enclosure == True)[0]
        index_NOT_enclosure = np.where(enclosure == False)[0]
        deq_F = np.array([sorted_cupules_objects[index].deq*scale_valor for index in index_enclosure])
        GA_F = np.array([sorted_cupules_objects[index].GA*scale_valor for index in index_enclosure])
        PA_F = np.array([sorted_cupules_objects[index].PA*scale_valor for index in index_enclosure])
        PA_O = np.array([sorted_cupules_objects[index].PA*scale_valor for index in index_NOT_enclosure])
        
        fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(nrows=3,ncols=2,figsize=(20,15))

        ax1.hist(surf, bins = 50, density=True, histtype='step', cumulative=True)
        ax1.set_title("Surfaces en freq. cumulees (m**2)")
        ax1.set_xlabel("Surfaces des cupules (m**2)")
        ax1.set_ylabel("Frequences")
                
        ax2.pie([len(index_enclosure), len(index_NOT_enclosure)], labels=["Cupules fermees","Cupules ouvertes"])
        
        ax3.hist(deq_F, bins = 50, density=True, histtype='step', cumulative=True)
        ax3.set_title("Diametres equivalents des cupules fermees en freq. cumulees (m)")
        ax3.set_xlabel("Diametres equivalents des cupules fermees (m)")
        ax3.set_ylabel("Frequences")
        
        ax4.hist(GA_F, bins = 50, density=True, histtype='step', cumulative=True)
        ax4.set_title("Grands axes des cupules fermees en freq. cumulees (m)")
        ax4.set_xlabel("Grands axes des cupules fermees (m)")
        ax4.set_ylabel("Frequences")
        
        ax5.hist(PA_F, bins = 50, density=True, histtype='step', cumulative=True)
        ax5.set_title("Petits axes des cupules fermees en freq. cumulees (m)")
        ax5.set_xlabel("Petits axes des cupules fermees (m)")
        ax5.set_ylabel("Frequences")
        
        ax6.hist(PA_O, bins = 50, density=True, histtype='step', cumulative=True)
        ax6.set_title("Petits axes des cupules ouvertes en freq. cumulees (m)")
        ax6.set_xlabel("Petits axes des cupules ouvertes (m)")
        ax6.set_ylabel("Frequences")
        
        plt.tight_layout(pad=3)
        plt.show()

        #Ecriture des resultats dans un fichier texte
        os.chdir(os.getcwd()+r'\results')
        try :
            #Effacage du fichier de resultats s'il existe deja
            os.remove(os.getcwd() + name_img + '_figs.png')
            os.remove(os.getcwd() + name_img + '.txt')
            fig.savefig(name_img + '_figs.png')
            with open(name_img+'.txt', 'w') as result:
                result.write(f"Image {name_img}; scale={scale_valor}; signal={signal_type}"+"\n")
                result.write("n°cupule; surface(m**2); fermeture_cupule(boolean); diametre_equivalent(m); grand_axe(m); petit_axe(m)"+"\n")
                for i, cupule in enumerate(sorted_cupules_objects):
                    result.write(f"{i+1}; {cupule.surface*scale_valor**2}; {cupule.fermee}; {cupule.deq*scale_valor}; {cupule.GA*scale_valor}; {cupule.PA*scale_valor}"+"\n")
        except : 
            fig.savefig(name_img + '_figs.png')
            with open(name_img+'.txt', 'w') as result:
                result.write(f"Image {name_img}; scale={scale_valor}; signal={signal_type}"+"\n")
                result.write("n°cupule; surface(m**2); fermeture_cupule(boolean); diametre_equivalent(m); grand_axe(m); petit_axe(m)"+"\n")
                for i, cupule in enumerate(sorted_cupules_objects):
                    result.write(f"{i+1}; {cupule.surface*scale_valor**2}; {cupule.fermee}; {cupule.deq*scale_valor}; {cupule.GA*scale_valor}; {cupule.PA*scale_valor}"+"\n")
            
        return(None)
        
    start_analysis = Button(fenetre, text="Lancer l'analyse", width=15, command=analysis)
    start_analysis.pack(side=BOTTOM)

    
    #Lancement de la routine (receptionnaire d'evenements)
    fenetre.mainloop()
    
    return(None)

###############################################################################
################################################ Main code
###############################################################################

############################################ Parametre a changer pour l'analyse
name_img = r'TSC_3_07'
###############################################################################

#accessing path
path = os.getcwd()+r'\\img_png\\'+name_img+r'.png'

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