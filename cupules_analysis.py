import numpy as np
import cv2 as cv

class Cupule:

    def __init__(self, points, img, border):
        self.points = points
        self.surface = len(points)
        self.imprint = self.isolation(img)
        self.border = border  #True si cupule en bordure d'image
        self.contour = self.contours()
        self.deq =  self.d_eq()
        Gaxe, Paxe = self.axes()
        self.GA = Gaxe
        self.PA = Paxe 
        self.fermee = self.fermeture(0.8)
        
    def isolation(self, img):
        imprint = np.zeros(np.shape(img))
        for (i, j) in self.points:
            imprint[i][j] = 255
        return imprint
    
    def contours(self):
        edges = cv.Canny(self.imprint, 50, 100)
        edges = cv.dilate(edges, None, iterations=1)
        edges = cv.erode(edges, None, iterations=1)
        cnts = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = cnts[0][0]
        return contours
    
    def d_eq(self):
        perimetre = cv.arcLength(self.contour,True)
        return 0.5 * (np.sqrt(4*self.surface/np.pi) + perimetre/np.pi)

    def axes(self):
        ellipse = cv.fitEllipse(self.contour)
        return ellipse[1][1], ellipse[1][0]

    def fermeture(self, seuil):
        hull = cv.convexHull(self.contour)
        ar = np.zeros(np.shape(self.imprint))
        cv.fillConvexPoly(ar, hull, 1)
        compteur_hull = 0
        for x in range(len(ar)):
            for y in range(len(ar[0])):
                if ar[x, y] == 1:
                    compteur_hull += 1
        if self.surface/compteur_hull >= seuil:
            return True
        else:
            return False
