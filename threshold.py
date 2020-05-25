import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import copy

def seuillage(path, threshold, group):
    def voisin(x,y):
        V = []
        if img_clean[y - 1][x] == 255:
            V += [(x,y-1)]
        if img_clean[y + 1][x] == 255:
            V += [(x,y+1)]
        if img_clean[y][x - 1] == 255:
            V += [(x-1,y)]
        if img_clean[y][x + 1] == 255:
            V += [(x+1,y)]
        return(V)
    
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        
    #Seuillage : attribution de 0 ou 255 a chaque pixel suivant sa valeur par rapport au seuil
    _,img_seuil = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO)
    _,img_seuil = cv2.threshold(img_seuil, 0, 255, cv2.THRESH_BINARY)
    
    cv2.imshow("image avec seuil",img_seuil)
    
    img_clean = copy.deepcopy(img_seuil)
    
    #Parcours de l'image a la recherche de groupes de pixels isoles (parasites)
    height, width = len(img_clean), len(img_clean[0])
    for x in range (3, width-3):
        for y in range(3, height-3):
            if img_clean[y][x] == 255:
                V = voisin(x,y)
                v = len(V)
                for i,j in V:
                    v += len(voisin(i,j))
                if v <= group:
                    img_clean[y][x] = 0
    
    cv2.imshow("image clean",img_clean)
    cv2.waitKey(0)
    
    return(None)

seuillage(r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Projet_cupules\img_png\3_TCS_AMB_2_m-s_20.png', 150, 4)