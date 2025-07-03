from donnees_en_df import df_dil, df_blanc, df_InRe, df_ech
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from correctionblancetsensib import dico_elt_corblancsensib

df_concentration = df_ech.copy()
a=0
for val in df_concentration.loc['115In']:
    coeffs = dico_elt_corblancsensib['115In'][int(np.array(df_ech.loc['numérotation_dilution'])[a]) - 1]
    col_name = df_concentration.columns[a]
    i=int(df_ech.loc['numérotation_blanc'].iloc[a]) - 1
    j=df_blanc.columns[i]
    df_concentration.loc['115In', col_name] = coeffs[0] * (val-df_blanc.loc['115In', j]) + coeffs[1]
    a+=1
for i in range(1, 9):
    elt = df_concentration.index[i]
    ligne_concentration = df_concentration.iloc[i]
    ligne_blanc = df_blanc.loc[elt]
    nom_ligne = df_concentration.index[i]
    if nom_ligne != '115In':
        for a, val in enumerate(ligne_concentration):
            # Obtenir les indices de dilution et de blanc à utiliser
            indice_dilution = int(df_ech.loc['numérotation_dilution'].iloc[a]) - 1
            indice_blanc = int(df_ech.loc['numérotation_blanc'].iloc[a]) - 1

            # Récupération du coefficient d'étalonnage
            coeffs = dico_elt_corblancsensib[elt][indice_dilution]

            # Correction du blanc
            nb_coup_corrige = ligne_concentration[a] - ligne_blanc.iloc[indice_blanc]

            # Correction de sensibilité par rapport à l'indium
            in_ech = df_ech.loc['115In'].iloc[a]
            in_blanc = df_blanc.loc['115In'].iloc[indice_blanc]
            in_mesure = df_concentration.loc['115In'].iloc[a]
            nb_coup_corrigesensib = (nb_coup_corrige / (in_ech - in_blanc)) * in_mesure
            print(in_mesure,i,a)
            # Mise à jour de la valeur corrigée
            df_concentration.iloc[i, a] = coeffs[0] * nb_coup_corrigesensib + coeffs[1]
         
    
print(df_concentration,df_ech)

'''for i in range(1,len(df_concentration)):
    a=0
    for val in df_concentration.iloc[i]:

        coeffs = dico_elt_corblancsensib[df_concentration.index[i]][int(np.array(df_ech.loc['numérotation_dilution'])[a]) - 1]

        nb_coup_corrige= df_concentration.iloc[i]-np.array(df_blanc.loc[df_concentration.index[i]])[int(np.array(df_ech.loc['numérotation_blanc'])[a]) - 1]
        nb_coup_corrigesensib = (nb_coup_corrige / (np.array(df_ech.loc['115In'])[a]-np.array(df_blanc.loc['115In'])[int(np.array(df_ech.loc['numérotation_blanc'])[a]) - 1]))* np.array(df_concentration.loc['115In'])[a]
        df_concentration.iloc[i, a] = coeffs[0] * nb_coup_corrigesensib + coeffs[1]
        a+=1
        print(a)'''

