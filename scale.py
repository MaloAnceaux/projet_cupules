import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import pyocr
import pyocr.builders


def scale2(path, x1, x2, y1, y2):
    pytesseract.pytesseract.tesseract_cmd = 'Lib/site-packages/pytesseract/tesseract/tesseract'
    
    area = (x1, y1, x2, y2)
    
    im = Image.open(path) # Ouverture du fichier image
    im = im.crop(area) #Rognage pour garder la partie contenant l'echelle
    
    # Filtrage (augmentation du contraste)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    
    # Lancement de la procedure de reconnaissance
    text = pytesseract.image_to_string(im)
    
    return(text)

def scale(path, x1, x2, y1, y2):
    
    tools = pyocr.get_available_tools()
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    
    langs = tool.get_available_languages()
    lang = langs[0]
    # Note that languages are NOT sorted in any way. Please refer
    # to the system locale settings for the default language
    # to use.
    
    area = (x1, y1, x2, y2)
    
    im = Image.open(path) # Ouverture du fichier image
    im = im.crop(area) # Rognage pour garder la partie contenant l'echelle

    txt = tool.image_to_string(
        im,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    # txt is a Python string
    
    return(txt)

print(scale(r'C:\Users\PULSAT\Documents\Mines\Transversalite\Info\Cupules\projet_cupules\img_png\3_TCS_AMB_2_m-s_20.png', 419, 652, 731, 768))