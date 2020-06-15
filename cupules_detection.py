critere_taille = 20
critere_surface = 3
import random as rd
import copy

def detection_cup(img):
    """
    img = image a explorer
    output = liste des cupules (liste de liste, et dans chaque sous liste des tuples decrivent les points de la cupule)
    """
    liste_cupules = []
    hauteur = len(img)
    largeur = len(img[0])
    for i in range(hauteur):
        for j in range(largeur):
            if img[i][j] == 0:
                liste_cupules.append(parcours_int_cupules(img, i, j))
    return liste_cupules


def parcours_int_cupules(img, i, j):
    """
    img = image a explorer
    output = liste des points constituant la cupule
    """
    hauteur = len(img)
    largeur = len(img[0])
    cupule = []
    cupule_a_faire = [(i, j)]
    c = 0
    couleur = rd.randint(5,250)
    while len(cupule_a_faire) > 0:
        c += 1
        n, p = cupule_a_faire[0]
        cupule += [(n, p)]
        img[n][p] = couleur
        del cupule_a_faire[0]
        if n + 1 < hauteur and p < largeur and img[n + 1][p] == 0:
            cupule_a_faire.append((n + 1, p))
            img[n + 1][p] = 1
        if n - 1 < hauteur and p < largeur and n > 0 and img[n - 1][p] == 0:
            cupule_a_faire.append((n - 1, p))
            img[n - 1][p] = 1
        if n < hauteur and p + 1 < largeur and img[n][p + 1] == 0:
            cupule_a_faire.append((n, p + 1))
            img[n][p + 1] = 1
        if n < hauteur and p - 1 < largeur and p > 0 and img[n][p - 1] == 0:
            cupule_a_faire.append((n, p - 1))
            img[n][p - 1] = 1
    return cupule

def discrimination_taille(liste_cupules, img):
    """
    liste_cupules = liste de cupules
    img = image
    output = trie des vraies cupules des fausses (i.e. l'espace entre 2 frontieres), en regardant les largeurs et hauteurs moyennes de toutes les cupules et en enlevant les valeurs extremes
    """
    largeur_cupules = []
    hauteur_cupules = []
    moy_largeur, moy_hauteur = 0, 0
    for cupule in liste_cupules:
        l, h = taille_cupule(cupule)
        largeur_cupules.append(l)
        hauteur_cupules.append(h)
    for largeur in largeur_cupules:
        moy_largeur += largeur
    moy_largeur = moy_largeur / len(largeur_cupules)
    for hauteur in hauteur_cupules:
        moy_hauteur += hauteur
    moy_hauteur = moy_hauteur / len(hauteur_cupules)
    lcopy = copy.deepcopy(liste_cupules)
    indice = 0
    for i, cupule in enumerate(lcopy):
        l, h = taille_cupule(cupule)
        if l < moy_largeur / critere_taille or l > moy_largeur * critere_taille or h < moy_hauteur / critere_taille or h > moy_hauteur * critere_taille :
            for point in liste_cupules[indice]:
                x, y = point[0], point[1]
                img[x][y] = 0
            del liste_cupules[indice]
        else : 
            indice += 1
    return liste_cupules

def taille_cupule(cupule):
    """
    cupule = liste des points contenus dans une cupule
    output = (largeur max, hauteur max) de la cupule
    """
    h_max = cupule[0][1]
    h_min = cupule[0][1]
    l_max = cupule[0][0]
    l_min = cupule[0][0]
    for (x, y) in cupule:
        if x > l_max :
            l_max = x
        elif x < l_min :
            l_min = x
        if y > h_max :
            h_max = y
        elif y < h_min :
            h_min = y
    return (l_max - l_min, h_max - h_min)

def discrimination_surface(liste_cupules, img):
    """
    liste_cupules = liste de cupules
    img = image
    output = trie des vraies cupules des fausses (i.e. l'espace entre 2 frontieres), en regardant les surfaces moyennes de toutes les cupules et en enlevant les valeurs extremes
    """
    surface_cupules = []
    moy_surfaces = 0
    for cupule in liste_cupules:
        surface = surface_cupule(cupule)
        surface_cupules.append(surface)
    for surface in surface_cupules:
        moy_surfaces += surface
    moy_surfaces = moy_surfaces / len(surface_cupules)
    for i, cupule in enumerate(liste_cupules):
        s = surface_cupule(cupule)
        if s < moy_surfaces / critere_surface or s > moy_surfaces * critere_surface:
            for point in liste_cupules[i]:
                x, y = point[0], point[1]
                img[x][y] = 0
            del liste_cupules[i]
    return liste_cupules

def surface_cupule(cupule):
    '''renvoie la surface d'une cupule'''
    return len(cupule)

def cleaner_cupule(liste_cupules):
    lcopy = copy.deepcopy(liste_cupules)
    l_supr = []
    for i, cupule in enumerate(lcopy):
        if surface_cupule(cupule) < surf_min_cup :
            l_supr += [i]
    for i in l_supr[::-1]:
        del liste_cupules[i]
