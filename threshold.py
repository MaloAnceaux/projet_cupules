import cv2
import copy

def img_threshold(img, threshold, group):
    """
    img = image a traiter
    threshold = valeur de seuillage (sur une echelle de gris allant de 0 a 255)
    group = nombre de pixels voisins d'un groupe limite amenant a sa suppression ou non (nettoyage des parasites)
    output = image opencv seuillee et nettoyee
    """
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
            
    #Seuillage : attribution de 0 ou 255 a chaque pixel suivant sa valeur par rapport au seuil
    _,img_seuil = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO)
    _,img_seuil = cv2.threshold(img_seuil, 0, 255, cv2.THRESH_BINARY)
    
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
    
    return(img_clean)

def find_threshold(img):
    """
    img = image a traiter
    output = seuillage moyen et renverse
    """
    nb_px = len(img)*len(img[0])
    sum_tot = sum([sum(l) for l in img])
    return( int(sum_tot/nb_px) )