# Développement d’un logiciel de traitement de données de laboratoire
## Hackaton 2025 - Mines Paris

### Projet :

Il s'agit d'exploiter des données obtenues lors d'expérimentations. L'objectif est de déterminer les concentrations de différents éléments dans des échantillons. Pour cela, la machine utilisée identifie un nombre de coûts de chaque élément dans un échantillon. Il faut ensuite convertir ce nombre en concentration. Pour cela on utilise des échantillons étalons plus ou moins dilués, et on fait une régression linéaire pour obtenir une fonction de conversion pour chaque élément. 

De plus, il faut corriger le bruit des mesures et la sensibilité de l'appareil. Pour cela, on utilise des échantillons "blancs", et des échantillons avec de l'indium et du rhénium.

### Travail effectué, par étape :

Pour chaque étape (exceptée l'étape préliminaire), les codes proposés ci-dessous sont dans l'ordre d'ajout de nouvelles fonctionnalités. Il est donc possible de n'exécuter que le dernier fichier pour obtenir l'information attendue (tracé ou dictionnaire).

1. Préliminaire : choix des élements considérés dans l'étude et import des tableaux excel

listeindex.py : listes des éléments à considérer d'après la consigne, ainsi que le nouveau nom à leur attribuer, et le nom qui leur est donné dans le fichier de concentrations étalons.

donnees_en_df.py : code qui ouvre les fichiers excels et les met sous forme de DataFrame en ne gardant que les informations nécessaires à l'étude.

2. Evolution du nombre de coûts au cours des expériences dans les blancs

evol_temp.py : trace l'évolution du nombre de coûts de chaque élément au cours des expériences, dans les blancs, les échantillons InRe, et les échantillons standards. Les variations donnent des informations sur les échantillons mesurés avant. Il faut mettre les graphes en grand écran pour bien voir les noms des axes. 

3. Conversion de nombre de coût en concentration : régression linéaire

reglin_etalon.py : crée un dictionnaire avec les paramètres de régression linéraire entre le nombre de coûts et la concentration de chaque étalon, pour chaque élément.  Trace les graphes de ces régressions.

reglin_etalon_interactif.py : comme le code précédent, mais avec la possibilité de cliquer sur un point sur un graphe pour le supprimer s'il parait faux ou lié à une erreur de mesure. Met à jour le graphe et les coefficients de la régression linéaire, stockées dans le dictionnaire.

4. Corrections des paramètres de régression linéaire : bruit et sensibilité de l'appareil

correctionblanc.py : même fonction que reglin_etalon mais en tenant compte de la correction à partir du blanc sur le nombre de coups. Renvoie donc les paramètres des régressions linéaires corrigées.

correctionblancetsensib.py : corrige en plus la sensibilité de l'appareil. Les paramètres de régression linéaire prendront donc cette correction supplémentaire.

correctionblancetsensib_interactif.py : comme le code précédent, mais avec la possibilité de cliquer sur un point sur un graphe pour le supprimer. Met à jour le graphe et les coefficients de la régression linéaire, stockées dans dico_elt_corblancsensib.

correctionblancetsensiblin_inter.py : comme le code précédent, mais avec une régression strictement linéaire (en passant par 0).

correctioninc.py : comme le code précédent mais en rajoutant les calculs d'incertitude.

5. Analyse des échantillons 

analyse_ech.py : crée une dataframe contenant les concentrations des éléments considérés de chaque échantillon et exporte un fichier excel contenant les concentrations.

analyse_echlin.py : comme le code précédent, mais avec une régression strictement linéaire (en passant par 0).

analyse_echlin_inc : exporte en plus le fichier excel contenant les incertitudes relatives

## Outils et librairies

Tout le code est en python et les modules utilisés sont dans le fichier requirements.txt .