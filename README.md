# Analyse d'images et détections de cupules
## Projet d'informatique - Mines ParisTech
### Réalisé par Léo SIMPLET - Malo ANCEAUX - Paul DHALLUIN
### pour aider le travail de thèse de Chloé VARENNE

La thèse de Chloé Varenne porte sur l'alliage base Titane Ti-Cr-Sn.
Le but de ce projet est de fournir à Chloé Varenne un programme permettant d'analyser des images de cupules issues d'un microscope électronique à balayage.
Les caractéritiques de ces cupules, formées lors de la fracture d'un échantillon, sont essentielles pour comprendre le mécanisme de fracture et prévoir le comportement du nouvel alliage.
Une interface graphique permet à l'utilisateur de choisir différents paramètres, et le programme fournit différents histogrammes illustrant les caractéristiques générales des cupules.

### Installation des différents modules
Les modules utilisés sont les suivants :  
tkinter  
ctypes  
**pytesseract**  
PIL (Image, ImageTk)  
**cv2** (aka opencv)  
numpy  
random  
matplotlib.pyplot  
copy  
os

Prérequis pour l'installation de **pytesseract** :
* télécharger le zip de pytesseract à l'adresse suivante https://github.com/UB-Mannheim/tesseract/wiki, puis l'installer
    * ou bien installer pytesseract grâce à l'exécutable précédemment téléchargé (il est dejà dans le dossier tesseract du dépôt github)
* copier le chemin d'accès de l'exécutable tesseract.exe ainsi créé et le coller dans le code main.py, au niveau de *pytesseract.pytesseract.tesseract_cmd*
sous forme de *raw string* dont la syntaxe est
```python
r'blablabla'
```

Avec une installation classique Anaconda, seuls les modules **pytesseract** et **cv2** doivent être installés par la méthode suivante (dans le PowerShell Anaconda) :
```python
pip install pytesseract
```
et pour cv2
```python
pip install opencv-python
```

### Utilisation du programme

* Modifier dans le fichier "main.py" le chemin d'accès de l'image à analyser.
* Une interface graphique s'ouvre lorsque vous exécutez le code.
* Vous pouvez choisir manuellement le seuillage afin de faire ressortir les frontières des cupules et en évitant les imperfection au centre des cupules (vous pouvez raffraichir l'image seuillée en cliquant sur "image seuillée").
* Une fois le seuillage réalisé, vous pouvez réaliser un nettoyage de l'image afin d'enlever les éventuelles imperfections. Vous pouvez choisir le nombre de pixels vosins minimum.
* Appliquer ensuite le filtre de Canny et lancez l'analyse
* Un histogramme en fréquence de cupules représentant la répartition de ces dernières apparait. La discrimination des cuules s'opérent en élaborant une surface moyenne des cupules, et en éjectant les cupules dont la surface est éloignée de x fois (trop grand ou trop petit) de cette moyenne. x est ici appelé "critère de surface". Vous pouvez choisir, à l'aide de l'histogramme des surfaces, d'ignorer un certain pourcentage de cupules trop grandes et trop petites dans le calcul de la moyenne afin qu'elle reflète la taille moyenne des vraies cupules.
* Vous pouvez avoir un aperçu de la discrimination des cupules en cliquant sur le bouton analyse.
* Lorsque vous pensez avoir bien isoler les cupules, vous pouvez lancer l'analyse en cliquant sur "lancer l'analyse". Une fenêtre avec les différents histogrammes demandés apparait.


Il faut noter que l'exécution du programme peut prendre un peu de temps (de l'ordre de la minute).



