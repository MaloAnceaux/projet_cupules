import cv2
import numpy as np

def hough_circles(img, param1, param2, minRadius, maxRadius):
    """
    img = image a traiter
    param1 = seuillage haut pour le gradient utilise dans le filtre de Canny (cf wiki)
    param2 = seuillage bas pour le gradient utilise dans le filtre de Canny (cf wiki)
    minRadius = rayon minimal des cercles a trouver (en pixels)
    maxRadius = rayon maximal des cercles a trouver (en pixels)
    """
    
    gray = cv2.medianBlur(img, 5)
    
    rows = gray.shape[0]
    
    #detection des cercles (circles est une liste des (x,y,r) correspondant a chaque cercle)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=param1, param2=param2,
                                minRadius=minRadius, maxRadius=maxRadius)
    
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    #dessin des cercles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(color, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(color, center, radius, (0, 0, 255), 3)
    
    return(color)