import random as rd

def detection_cup(img):
    liste_cupules = []
    hauteur = len(img)
    largeur = len(img[0])
    for i in range(hauteur):
        for j in range(largeur):
            if img[i][j] == 0:
                liste_cupules.append(parcours_int_cupules(img, i, j))
    return liste_cupules


def parcours_int_cupules(img, i, j):
    '''retourne la liste des points constituant la cupule'''
    hauteur = len(img)
    largeur = len(img[0])
    cupule = []
    cupule_a_faire = [(i, j)]
    c = 0
    couleur = rd.randint(5,250)
    while len(cupule_a_faire) > 0:
        c += 1
        n, p = cupule_a_faire[0]
        cupule += (n, p)
        img[n][p] = couleur
        del cupule_a_faire[0]
        if n + 1 < hauteur and p < largeur and img[n + 1][p] == 0:
            cupule_a_faire.append((n + 1, p))
            img[n + 1][p] = 1
        if n - 1 < hauteur and p < largeur and img[n - 1][p] == 0:
            cupule_a_faire.append((n - 1, p))
            img[n - 1][p] = 1
        if n < hauteur and p + 1 < largeur and img[n][p + 1] == 0:
            cupule_a_faire.append((n, p + 1))
            img[n][p + 1] = 1
        if n < hauteur and p - 1 < largeur and img[n][p - 1] == 0:
            cupule_a_faire.append((n, p - 1))
            img[n][p - 1] = 1
    return cupule

def elimination_frontieres(liste_cupules):
    '''permet de discriminer les vraies cupules des fausses (i.e. l'espace entre 2 frontières), en regardant les largeurs et hauteurs moyennes de toutes les cupules et en enlevant les valeur extrêmes'''
    largeur_cupules = []
    hauteur_cupules = []
    for cupule in liste_cupules:
        l, h = taille_cupule(cupule)
        largeur_cupules.append(l)
        hauteur_cupule.append(h)
    for largeur in largeur_cupules:
        moy_largeur += largeur
    moy_largeur = moy_largeur / len(largeur_cupules)
    for hauteur in hauteur_cupules:
        moy_hauteur += hauteur
    moy_hauteur = moy_hauteur / len(hauteur_cupules)
    

def taille_cupule(cupule):
    '''renvoie (largeur max, hauteur max) de cupule'''
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
