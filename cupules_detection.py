import numpy as np
import random as rd
import copy
import numpy as np
import cv2

#les cupules avec une surface inferieure a surf_min_cup sont ecartees d'office
surf_min_cup = 20  

###############################################################################
################################################ Class Cupule
###############################################################################

class Cupule:
    def __init__(self, points, img, border):
        self.points = points
        self.surface = len(points)
        self.imprint = self.isolation(img)
        self.border = border  #True si cupule en bordure d'image
        self.contour = None
        self.deq =  None
        Gaxe, Paxe = None, None
        self.GA = Gaxe
        self.PA = Paxe 
        self.fermee = None
        
    def isolation(self, img):
        imprint = np.zeros(np.shape(img))
        for (i, j) in self.points:
            imprint[i][j] = 255
        return imprint
    
    def contours(self):
        impcopy = np.uint8(self.imprint)
        edges = cv2.Canny(impcopy, 50, 100, 3)
        edges = cv2.dilate(edges, None, iterations=1)
        edges = cv2.erode(edges, None, iterations=1)
        cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = cnts[0][0]
        return contours
    
    def d_eq(self):
        perimetre = cv2.arcLength(self.contour,True)
        return 0.5 * (np.sqrt(4*self.surface/np.pi) + perimetre/np.pi)

    def axes(self):
        if len(self.contour) < 5:
            return(0, 0)
        else:
            ellipse = cv2.fitEllipse(self.contour)
            return ellipse[1][1], ellipse[1][0]

    def fermeture(self, seuil):
        hull = cv2.convexHull(self.contour)
        ar = np.zeros(np.shape(self.imprint))
        cv2.fillConvexPoly(ar, hull, 1)
        compteur_hull = 0
        for x in range(len(ar)):
            for y in range(len(ar[0])):
                if ar[x, y] == 1:
                    compteur_hull += 1
        if self.surface/compteur_hull >= seuil:
            return True
        else:
            return False

###############################################################################
################################################ Functions
###############################################################################

def refresh_affichage_cupules(liste_detec, img, pourcentage_surface_max, pourcentage_surface_min, critere_surface):
    '''raffraichis l'affichage des cupules et discrimine les cupules avec les paramètres de pourcentages et de critère'''
    new_im = copy.deepcopy(img)
    new_im2 = copy.deepcopy(img)
    new_im = color_black(new_im, liste_detec)
    liste_discr, img_finale = discrimination_surface(liste_detec, new_im2, pourcentage_surface_max, pourcentage_surface_min, critere_surface)
    new_im = color_random(new_im, liste_discr)
    return liste_discr, new_im, img_finale

def detection_cup(img):
    """
    img = image a explorer
    output = liste des cupules (liste d'objets Cupule)
    """
    liste_cupules = []
    hauteur = len(img)
    largeur = len(img[0])
    for i in range(hauteur):
        for j in range(largeur):
            if img[i][j] == 0:
                liste_cupules.append(parcours_int_cupules(img, i, j))
    liste_cupules = del_cupule_border(liste_cupules)
    return liste_cupules

def parcours_int_cupules(img, i, j):
    """
    img = image a explorer
    output = liste des points constituant la cupule
    """
    hauteur = len(img)
    largeur = len(img[0])
    cupule = []
    pixel_a_faire = [(i, j)]
    c = 0
    border = False
    while len(pixel_a_faire) > 0:
        c += 1
        n, p = pixel_a_faire[0]
        cupule += [(n, p)]
        del pixel_a_faire[0]
        if n + 1 < hauteur and p < largeur and img[n + 1][p] == 0:
            pixel_a_faire.append((n + 1, p))
            img[n + 1][p] = 1
        if n - 1 < hauteur and p < largeur and n > 0 and img[n - 1][p] == 0:
            pixel_a_faire.append((n - 1, p))
            img[n - 1][p] = 1
        if n < hauteur and p + 1 < largeur and img[n][p + 1] == 0:
            pixel_a_faire.append((n, p + 1))
            img[n][p + 1] = 1
        if n < hauteur and p - 1 < largeur and p > 0 and img[n][p - 1] == 0:
            pixel_a_faire.append((n, p - 1))
            img[n][p - 1] = 1
        if n + 1 > hauteur or p + 1 > largeur:
            border = True
    return Cupule(cupule, img, border)

def color_random(img, liste):
    '''colorie les cupules de liste en niveau de gris aléatoire'''
    for cupule in liste:
        couleur = rd.randint(30, 220)
        for point in cupule.points:
            x, y = point[0], point[1]
            img[x][y] = couleur
    return img

def color_black(img, liste):
    '''colorie les cupules de liste en noir'''
    for cupule in liste:
        couleur = 1
        for point in cupule.points:
            x, y = point[0], point[1]
            img[x][y] = couleur
    return img

def discrimination_surface(liste_cupules, img, pourcentage_surface_max, pourcentage_surface_min, critere_surface):
    """
    liste_cupules = liste de cupules
    img = image a traiter
    pourcentage_surface_max = pourcentage des cupules (les plus grandes en surface) qui sont ecartees dans le calcul de la moyenne
    pourcentage_surface_min = pourcentage des cupules (les plus petites en surface) qui sont ecartees dans le calcul de la moyenne
    critere_surface = permet de garder les cupules dont la surface est critere_surface fois inferieure/superieure à la moyenne des tailles
    output = trie des vraies cupules des fausses (i.e. l'espace entre 2 frontieres), en regardant les surfaces moyennes de toutes les cupules et en enlevant les valeurs extremes
    """
    liste_cupules = cleaner_cupule(liste_cupules)
    surfaces_cupules = []
    for i, cupule in enumerate(liste_cupules):
        surface = cupule.surface
        surfaces_cupules.append((surface, i))
    surfaces_cupules.sort()
    n = len(surfaces_cupules)
    del surfaces_cupules[int((1 - pourcentage_surface_max/100) * n):]
    del surfaces_cupules[:int(pourcentage_surface_min/100 * n)]
    moy_surfaces = moyenne(surfaces_cupules)
    lcopy = copy.deepcopy(np.array(liste_cupules))
    indice = 0
    for cupule in lcopy:
        s = cupule.surface
        if s < moy_surfaces / critere_surface or s > moy_surfaces * critere_surface:
            for point in liste_cupules[indice].points:
                x, y = point[0], point[1]
                img[x][y] = 0
            del liste_cupules[indice]
        else :
            indice += 1
    return liste_cupules, img

def moyenne(L):
    '''renvoie la moyenne des elements de L'''
    if len(L) == 0:
        return 0
    else :
        m = 0
        for element in L:
            m += element[0]
        return m / len(L)

def cleaner_cupule(liste_cupules):
    '''elimine d'office les cupules dont la surface est inferieure a surf_min_cup'''
    l_supr = []
    for i, cupule in enumerate(liste_cupules):
        if cupule.surface < surf_min_cup :
            l_supr += [i]
    for i in l_supr[::-1]:
        del liste_cupules[i]
    return liste_cupules

def del_cupule_border(liste_cupules):
    '''enleve de liste_cupules les cupules en contact avec la bordure de l'image (taille inestimable donc peu fiable)'''
    indice_del = []
    for i, cupule in enumerate(liste_cupules):
        if cupule.border:
            indice_del += [i]
    for indice in indice_del[::-1]:
        del liste_cupules[indice]
    return liste_cupules