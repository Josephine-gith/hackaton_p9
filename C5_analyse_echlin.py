import numpy as np
import matplotlib.pyplot as plt

from C1_donnees_en_df import df_blanc, df_ech
from C4_correctionblancsensiblin_inter import dico_elt_corblancsensib

# Copie du dataframe d'échantillons pour modifier les valeurs et y mettre les concentrations
df_concentration = df_ech.copy()
a = 0

# Calcul de la concentration de l'indium dans les échantillons en utilisant donc uniquement la correction du blanc
for val in df_concentration.loc["115In"]:
    coeffs = dico_elt_corblancsensib[
        "115In"
    ][
        int(np.array(df_ech.loc["numérotation_dilution"])[a])
        - 1  # Choisit le bon coefficient suivant après quel échantillon standardisé l'expérience a été faite
    ]
    col_name = df_concentration.columns[a]  # Nom de la colonne de l'échantillon
    i = (
        int(np.array(df_ech.loc["numérotation_blanc"])[a]) - 1
    )  # Numéro de l'échantillon blanc précédent (pour la correction)
    j = df_blanc.columns[i]
    df_concentration.loc["115In", col_name] = coeffs * (
        val - df_blanc.loc["115In", j]
    )  # Insert la concentration d'indium dans la dataframe
    a += 1

# Correction des autres éléments en fonction de l'indium
for i in range(1, 9):
    elt = df_concentration.index[i]  # Nom de l'élément
    ligne_concentration = df_concentration.iloc[
        i
    ]  # Ligne de l'élément dans la dataframe
    ligne_blanc = df_blanc.loc[elt]  # Ligne de l'élément dans la dataframe des blancs
    nom_ligne = df_concentration.index[
        i
    ]  # Nom de la ligne de l'élément dans la dataframe
    # On ne corrige pas l'indium, il a déjà été corrigé
    if nom_ligne != "115In":
        for a, val in enumerate(ligne_concentration):
            # Obtenir les indices de dilution et de blanc à utiliser
            indice_dilution = int(np.array(df_ech.loc["numérotation_dilution"])[a]) - 1
            indice_blanc = int(np.array(df_ech.loc["numérotation_blanc"])[a]) - 1

            # Récupération du coefficient d'étalonnage
            coeffs = dico_elt_corblancsensib[elt][indice_dilution]

            # Correction du blanc
            nb_coup_corrige = ligne_concentration[a] - ligne_blanc.iloc[indice_blanc]

            # Correction de sensibilité par rapport à l'indium
            in_ech = df_ech.loc["115In"].iloc[a]
            in_blanc = df_blanc.loc["115In"].iloc[indice_blanc]
            in_mesure = df_concentration.loc["115In"].iloc[a]
            nb_coup_corrigesensib = (nb_coup_corrige / (in_ech - in_blanc)) * in_mesure
            print(in_mesure, i, a)
            # Mise à jour de la valeur corrigée
            df_concentration.iloc[i, a] = coeffs * nb_coup_corrigesensib

# Affichage de la dataframe des concentrations corrigées
print(df_concentration)

df_concentration.drop(
    ["numérotation_dilution", "numérotation_blanc", "numérotation_derive"], inplace=True
)  # Suppression des lignes inutiles
df_concentration.to_excel("data/concentration_corrigeelin.xlsx", index=True)
