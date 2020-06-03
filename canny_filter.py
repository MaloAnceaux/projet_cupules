import cv2

def canny_threshold(img, low_threshold, up_threshold, kernel_size = 3):
    """
    img = image a traiter
    low_threshold = seuillage haut pour le gradient utilise dans le filtre de Canny (cf wiki)
    up_threshold = seuillage bas pour le gradient utilise dans le filtre de Canny (cf wiki)
    """
    gray = cv2.medianBlur(img, 5)
    detected_edges = cv2.Canny(gray, low_threshold, up_threshold, kernel_size)
    return(detected_edges)