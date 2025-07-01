from donnees_en_df import df_dil
from listeindex import lis_index_2
import pandas as pd
import numpy as np


xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_2025.xls")
df_factdil = pd.read_excel(xls, "indication_nom_echts", header=9)
df_factdil.drop(["Unnamed: 2", "Unnamed: 3"], axis=1, inplace=True)

df_etalon = pd.read_excel(xls, "solution-sdt_etalon", header=1)
df_etalon = df_etalon[df_etalon["Elément"].isin(lis_index_2)].reset_index(drop=True)
df_etalon.drop(
    [
        "concentration certifiée (ppb)",
        "Incertitude (±)",
        "Concentration théorique (ppb)",
    ],
    axis=1,
    inplace=True,
)

for dil in {0, 3, 10, 30, 100}:
    temp = df_factdil[df_factdil["Standard étalon"] == f"ET-DIL{dil}-04-A"]
    df_etalon[f"Concentration étalon dilué {dil}"] = np.array(
        df_etalon["Concentration étalon (ppb)"]
    ) * np.array(temp["Facteur de dilution"])

print(df_etalon)
