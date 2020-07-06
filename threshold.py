import cv2
import copy

def img_threshold(img, threshold):
    """
    img = image a traiter
    threshold = valeur de seuillage (sur une echelle de gris allant de 0 a 255)
    group = nombre de pixels voisins d'un groupe limite amenant a sa suppression ou non (nettoyage des parasites)
    output = image opencv seuillee et nettoyee
    """    
    img_clean = copy.deepcopy(img)
    
    #Seuillage : attribution de 0 ou 255 a chaque pixel suivant sa valeur par rapport au seuil
    _,img_clean = cv2.threshold(img_clean, threshold, 255, cv2.THRESH_TOZERO)
    _,img_clean = cv2.threshold(img_clean, 0, 255, cv2.THRESH_BINARY)
    
    return(img_clean)

def cleaner_threshold(img, group):
    """
    img = image a traiter
    group = nombre de voisin
    output = image nettoyee
    """
    new_img = copy.deepcopy(img)
    
    def voisin(x,y):
        V = []
        if img[y - 1][x] == 255:
            V += [(x,y-1)]
        if img[y + 1][x] == 255:
            V += [(x,y+1)]
        if img[y][x - 1] == 255:
            V += [(x-1,y)]
        if img[y][x + 1] == 255:
            V += [(x+1,y)]
        return(V)

    #Parcours de l'image a la recherche de groupes de pixels isoles (parasites)
    height, width = len(img), len(img[0])
    for x in range (3, width-3):
        for y in range(3, height-3):
            if img[y][x] == 255:
                V = voisin(x,y)
                v = len(V)
                for i,j in V:
                    v += len(voisin(i,j))
                if v <= group:
                    new_img[y][x] = 0
    return(new_img)

def find_threshold(img):
    """
    img = image a traiter
    output = seuillage moyen et renverse
    """
    nb_px = len(img)*len(img[0])
    sum_tot = sum([sum(l) for l in img])
    return( int(sum_tot/nb_px) )