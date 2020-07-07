# Analyse d'images et détections de cupules
## Projet d'informatique - Mines ParisTech
### Réalisé par Léo SIMPLET - Malo ANCEAUX - Paul DHALLUIN
### pour aider le travail de thèse de Chloé VARENNE

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
