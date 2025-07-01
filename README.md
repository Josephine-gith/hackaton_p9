# Développement d’un logiciel de traitement de données de laboratoire
## Hackaton 2025 - Mines Paris

A quoi correspond les différents fichiers python :
* listeindex.py : listes des éléments à considérer d'après la consigne, ainsi que le nouveau nom à leur attribuer, et le nom qui leur est donné dans le fichier de concentrations étalons.
* donnees_en_df.py : code qui ouvre les fichiers excels, les met sous forme de DataFrame en ne gardant que les informations nécessaires à l'étude.
* reglin_etalon.py : crée un dictionnaire avec les paramètres de régression linéraire entre le nombre de coûts et la concentration de chaque étalon, pour chaque élément.  Trace les graphes de ces régressions.

