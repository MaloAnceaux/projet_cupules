import pytesseract
from PIL import Image

def text_recognition(img, x1, x2, y1, y2):
    """
    img = image a analyser
    x1, y1 = coo du coin en haut a gauche du rectangle a etudier
    x2, y2 = coo du coin en bas a droite du rectangle a etudier
    output = texte contenu dans ce rectangle
    """
    area = (x1, y1, x2, y2)
    
    img_pil = Image.fromarray(img)
    img_pil = img_pil.crop(area) #Rognage pour garder la partie contenant l'echelle
    txt = pytesseract.image_to_string(img_pil)
    
    return(txt)

def scale(txt, nb_pixel):
    """
    txt = texte reconnu dans la zone d'echelle
    output = echelle en m/pixels
    """
    #passage en minuscules
    filtered_txt = txt.lower()
    
    l = filtered_txt.split()
    
    dic = {'nm' : 10**-9, 'um' : 10**-6, 'ym' : 10**-6, 'mm' : 10**-3}
    
    return(float(l[2])*dic[l[3]] / nb_pixel)

def signal(txt):
    """
    txt = texte reconnu dans la zone de signal
    output = nom du signal
    """
    #passage en minuscules
    filtered_txt = txt.lower()
    
    l = filtered_txt.split()
    
    return(l[2])
    
    