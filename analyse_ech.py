from donnees_en_df import df_dil, df_blanc, df_InRe, df_ech
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from correctionblancetsensib import dico_elt_corblancsensib

df_concentration = df_ech.copy()
a=0
print(a)
for val in df_concentration.loc['115In']:
    coeffs = dico_elt_corblancsensib['115In'][int(np.array(df_ech.loc['numérotation_dilution'])[a]) - 1]
    col_name = df_concentration.columns[a]
    df_concentration.loc['115In', col_name] = coeffs[0] * val + coeffs[1]

    a+=1

for i in range(1,len(df_concentration)):
    a=0
    for val in df_concentration.iloc[i]:

        coeffs = dico_elt_corblancsensib[df_concentration.index[i]][int(np.array(df_ech.loc['numérotation_dilution'])[a]) - 1]

        nb_coup_corrige= df_concentration.iloc[i]-np.array(df_blanc.loc[df_concentration.index[i]])[int(np.array(df_ech.loc['numérotation_blanc'])[a]) - 1]
        nb_coup_corrigesensib = (nb_coup_corrige / (np.array(df_ech.loc['115In'])[a]-np.array(df_blanc.loc['115In'])[int(np.array(df_ech.loc['numérotation_blanc'])[a]) - 1]))* np.array(df_concentration.loc['115In'])[a]
        df_concentration.iloc[i, a] = coeffs[0] * nb_coup_corrigesensib + coeffs[1]
        a+=1
print(a)
print(df_concentration, df_ech)
