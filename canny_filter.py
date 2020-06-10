import cv2
import copy

def canny_threshold(img, low_threshold, up_threshold, kernel_size = 3):
    """
    img = image a traiter
    low_threshold = seuillage haut pour le gradient utilise dans le filtre de Canny (cf wiki)
    up_threshold = seuillage bas pour le gradient utilise dans le filtre de Canny (cf wiki)
    Output = img filtree grace au filtre de Canny
    """
    gray = cv2.medianBlur(img, 5)
    detected_edges = cv2.Canny(gray, low_threshold, up_threshold, kernel_size)
    return(detected_edges)

def enlarge_border(img):
    img_elargie = copy.deepcopy(img)
    hauteur = len(img)
    largeur = len(img[0])
    for i in range(hauteur):
        for j in range(largeur):
            if img[i][j] == 255:
                if i + 1 < hauteur and j < largeur:
                    img_elargie[i + 1][j] = 255
                if i - 1 < hauteur and j < largeur and i > 0:
                    img_elargie[i - 1][j] = 255
                if i < hauteur and j + 1 < largeur:
                    img_elargie[i][j + 1] = 255
                if i < hauteur and j - 1 < largeur and j > 0:
                    img_elargie[i][j - 1] = 255
    return(img_elargie)