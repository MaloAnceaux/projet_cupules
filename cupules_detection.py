def detection_cup(img):
    liste_cupules = []
    hauteur = len(img)
    largeur = len(img[0])
    for i, j in (hauteur, largeur):
        if img[i][j] == 0:
            liste_cupules.append(parcours_int_cupules(img, i, j))
    return liste_cupules


def parcours_int_cupules(img, i, j):
    '''retourne la liste des points constituant la cupule'''
    cupule = []
    cupule_a_faire = [(i, j)]
    while len(cupule_a_faire) > 0:
        n, p = cupule_a_faire[0]
        cupule += parcours_rec(img, k, l)
        img[n][p] = 128
        del cupule_a_faire[0]
        if img[n + 1][p] == 0:
            cupule_a_faire.append((n + 1, p))
        if img[n - 1][p] == 0:
            cupule_a_faire.append((n - 1, p))
        if img[n][p + 1] == 0:
            cupule_a_faire.append((n, p + 1))
        if img[n][p - 1] == 0:
            cupule_a_faire.append((n, p - 1))