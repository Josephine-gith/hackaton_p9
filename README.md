# Développement d’un logiciel de traitement de données de laboratoire
## Hackaton 2025 - Mines Paris

A quoi correspond les différents fichiers python :
* listeindex.py : listes des éléments à considérer d'après la consigne, ainsi que le nouveau nom à leur attribuer, et le nom qui leur est donné dans le fichier de concentrations étalons.
* donnees_en_df.py : code qui ouvre les fichiers excels, les met sous forme de DataFrame en ne gardant que les informations nécessaires à l'étude.
* reglin_etalon.py : crée un dictionnaire avec les paramètres de régression linéraire entre le nombre de coûts et la concentration de chaque étalon, pour chaque élément.  Trace les graphes de ces régressions.
* evol_temp.py : trace l'évolution du nombre de coûts de chaque élément au cours des expériences, dans les blancs, les échantillons InRe, et les échantillons standards.
* correctionblanc.py : même fonction que reglinetalon mais en tenant compte de la correction à partir du blanc sur le nombre de coups, renvoie donc les paramètres et la régression linéaire corrigée.
* correctionblanc+sensib.py : corrige en plus la sensibilité, les paramètres de régression linéaire prendront donc cette correction.