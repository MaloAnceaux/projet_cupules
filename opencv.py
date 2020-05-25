import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt

def circle_opencv():
    #chemin d'acces et ouverture avec les trois channels de couleurs
    path = r'C:\Users\PULSAT\Documents\Mines\Transversalité\Info\Projet_cupules\img\3_TCS_AMB_2_m-s_19.TIFF'
    img = cv2.imread(path, 1)
    
    # #conversion en nuances de gris
    # gray = cv2.cvtColor(img, cv.COLOR_RGB2GRAY)
    # 
    # gray = cv2.medianBlur(gray, 5)
    # 
    # 
    # rows = gray.shape[0]
    # 
    # #detection des cercles (circles est une liste des (x,y,r) correspondant a chaque cercle)
    # circles = cv2.trtHoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
    #                             param1=100, param2=50,
    #                             minRadius=1, maxRadius=80)
    # 
    # #dessin des cercles
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         center = (i[0], i[1])
    #         # circle center
    #         cv2.circle(img, center, 1, (0, 100, 100), 3)
    #         # circle outline
    #         radius = i[2]
    #         cv2.circle(img, center, radius, (0, 0, 255), 3)
    
    #affichage dans la fenetre
    cv2.imshow("detected circles", img)
    cv2.waitKey(0)
    return(None)


