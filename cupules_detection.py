#définition des variables globales

critere_taille = 20 # garde les cupules dont la taille est critere_taille fois inférieur/supérieur à la moyenne des tailles
critere_surface = 9 # garde les cupules dont la surface est critere_surface fois inférieur/supérieur à la moyenne des tailles

pourcentage_taille_min  = 0.4 # pourcentage des cupules les plus petites en taille qui sont écartées dans le calcul de la moyenne
pourcentage_taille_max = 0.01 # pourcentage des cupules les plus grandes en taille qui sont écartées dans le calcul de la moyenne

pourcentage_surface_min = 0.4 # pourcentage des cupules les plus petites en surface qui sont écartées dans le calcul de la moyenne
pourcentage_surface_max = 0.01 # pourcentage des cupules les plus grandes en surface qui sont écartées dans le calcul de la moyenne

surf_min_cup = 20  # les cupules avec une surface inférieur à surf_min_cup sont écartées d'office

#importation des modules

import random as rd
import copy
from main import Cupule

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
    liste_discr = discrimination_surface(liste_cupules, img)
    return liste_discr

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
    border = False
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
        if n + 1 > hauteur or p + 1 > largeur:
            border = True
    return Cupule(cupule, img, border)

# def discrimination_taille(liste_cupules, img):
#     """
#     liste_cupules = liste de cupules
#     img = image
#     output = tri des vraies cupules des fausses (i.e. l'espace entre 2 frontieres), en regardant les largeurs et hauteurs moyennes de toutes les cupules et en enlevant les valeurs extremes
#     """
#     liste_cupules = cleaner_cupule(liste_cupules)
#     largeur_cupules = []
#     hauteur_cupules = []
#     for cupule in liste_cupules:
#         l, h = taille_cupule(cupule.points)
#         largeur_cupules.append(l)
#         hauteur_cupules.append(h)
#     largeur_cupules = largeur_cupules.sort()
#     hauteur_cupules = hauteur_cupules.sort()
#     n = len(largeur_cupules)
#     del largeur_cupules[:int(pourcentage_taille_min * n)]
#     del hauteur_cupules[:int(pourcentage_taille_min * n)]
#     del largeur_cupules[int((1 - pourcentage_taille_max) * n):]
#     del hauteur_cupules[int((1 - pourcentage_taille_max) * n):]
#     moy_largeur = moyenne(largeur_cupules)
#     moy_hauteur = moyenne(hauteur_cupules)
#     lcopy = copy.deepcopy(liste_cupules)
#     indice = 0
#     for cupule in lcopy:
#         l, h = taille_cupule(cupule.points)
#         if l < moy_largeur / critere_taille or l > moy_largeur * critere_taille or h < moy_hauteur / critere_taille or h > moy_hauteur * critere_taille :
#             for point in liste_cupules[indice].points:
#                 x, y = point[0], point[1]
#                 img[x][y] = 0
#             del liste_cupules[indice]
#         else :
#             indice += 1
#     return liste_cupules
#
#
#
# def taille_cupule(cupule):
#     """
#     cupule = liste des points contenus dans une cupule
#     output = (largeur max, hauteur max) de la cupule
#     """
#     # initialisation des min et max
#     h_max, h_min = cupule[0][1], cupule[0][1]
#     l_max, l_min = cupule[0][0], cupule[0][0]
#     for (x, y) in cupule:
#         if x > l_max :
#             l_max = x
#         elif x < l_min :
#             l_min = x
#         if y > h_max :
#             h_max = y
#         elif y < h_min :
#             h_min = y
#     return (l_max - l_min, h_max - h_min)


def discrimination_surface(liste_cupules, img):
    """
    liste_cupules = liste de cupules
    img = image
    output = trie des vraies cupules des fausses (i.e. l'espace entre 2 frontieres), en regardant les surfaces moyennes de toutes les cupules et en enlevant les valeurs extremes
    """
    liste_cupules = cleaner_cupule(liste_cupules)
    surfaces_cupules = []
    for i, cupule in enumerate(liste_cupules):
        surface = cupule.surface
        surfaces_cupules.append((surface, i))
    surfaces_cupules.sort()
    n = len(surfaces_cupules)
    l_index = []
    del surfaces_cupules[:int(pourcentage_surface_min * n)]
    del surfaces_cupules[int((1 - pourcentage_surface_max) * n)]
    moy_surfaces = moyenne(surfaces_cupules)
    lcopy = copy.deepcopy(liste_cupules)
    indice = 0
    for cupule in lcopy:
        s = cupule.surface
        if s < moy_surfaces / critere_surface or s > moy_surfaces * critere_surface:
            for point in liste_cupules[indice]:
                x, y = point[0], point[1]
                img[x][y] = 0
            del liste_cupules[indice]
        else :
            indice += 1
    return liste_cupules


def moyenne(L):
    '''renvoie la moyenne des éléments de L'''
    if len(L) == 0:
        return 0
    else :
        m = 0
        for element in L:
            m += element
        return m / len(L)


def cleaner_cupule(liste_cupules):
    '''élimine d'office les cupules dont la surface est inférieur à surf_min_cup'''
    l_supr = []
    for i, cupule in enumerate(liste_cupules):
        if cupules.surface < surf_min_cup :
            l_supr += [i]
    for i in l_supr[::-1]:
        del liste_cupules[i]
    return liste_cupules


def del_cupule_border(liste_cupules):
    '''enlève de liste_cupules les cupules en contact avec la bordure de l'image (taille inestimable donc peu fiable)'''
    indice_del = []
    for i, cupule in enumerate(liste_cupules):
        if cupule.border:
            indice_del += [i]
    for indice in indice_del[::-1]:
        del liste_cupules[indice]
    return liste_cupules