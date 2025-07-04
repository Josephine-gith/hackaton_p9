# Import de modules utiles
import pandas as pd
import numpy as np

## Traitement du document avec les mesures faites par l'appareil

# Import des données
from C1_liste_elements import lis_index, lis_name, lis_index_2

xls = pd.ExcelFile("data/Fichier_donnees_ICP-MS_projets-Mines_2025.xls")
df = pd.read_excel(xls, "resultats_bruts_ICP-MS")

# Selection des données intéressantes du DataFrame
df.dropna(axis=1, how="any", inplace=True)
df = df[df["File:"].isin(lis_index)].reset_index(drop=True)

# Changement d'indexation du DataFrame
df["File:"] = lis_name
df.set_index(df["File:"], inplace=True)
df.drop("File:", axis=1, inplace=True)

# Numérotation des expériences dans l'ordre chronologique et par groupe
i, j = 0, 0
numérotation_dilution = []
for k, elt in enumerate(df.loc["Sample"]):
    if elt == "ET-DIL100-04-A":
        i += 1
        j = k
    numérotation_dilution.append(i + (k - j) / 100)
df.loc["numérotation_dilution"] = numérotation_dilution

i, j = 0, 0
numérotation_derive = []
for k, elt in enumerate(df.loc["Sample"]):
    if elt == "InRe-A":
        i += 1
        j = k
    numérotation_derive.append(i + (k - j) / 100)
df.loc["numérotation_derive"] = numérotation_derive

i, j = 0, 0
numérotation_blanc = []
for k, elt in enumerate(df.loc["Sample"]):
    if elt == "HNO3 [0.37N]":
        i += 1
        j = k
    numérotation_blanc.append(i + (k - j) / 100)
df.loc["numérotation_blanc"] = numérotation_blanc

# Création de DataFrame séparés par 'Sample'
# blancs, standards dilués, InRe (mesure de dérive d'appareil)
df_blanc = df.loc[:, df.loc["Sample"] == "HNO3 [0.37N]"]
df_dil = df.loc[:, df.loc["Sample"].str.contains("DIL")]
df_derive = df.loc[:, df.loc["Sample"] == "InRe-A"]
# mesures de l'expérience
df_ech_intermediaire1 = df.drop(columns=df_dil.columns)
df_ech_intermediaire2 = df_ech_intermediaire1.drop(columns=df_blanc.columns)
df_ech = df_ech_intermediaire2.drop(columns=df_derive.columns)

## Traitement du document

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_20252.xls")

# Mise en forme des donnees
df_InRe = pd.read_excel(xls, "solution-sdt_InRe", header=6)
df_facteur_dilution = pd.read_excel(xls, "indication_nom_echts", header=9)
df_facteur_dilution.drop(["Unnamed: 2", "Unnamed: 3"], axis=1, inplace=True)
df_etalon = pd.read_excel(xls, "solution-sdt_etalon", header=1)
df_etalon = df_etalon[df_etalon["Elément"].isin(lis_index_2)].set_index("Elément")
df_etalon.drop(
    [
        "concentration certifiée (ppb)",
        "Incertitude (±)",
        "Concentration théorique (ppb)",
    ],
    axis=1,
    inplace=True,
)

for dil in [100, 30, 10, 3, 0]:
    temp = df_facteur_dilution[
        df_facteur_dilution["Standard étalon"] == f"ET-DIL{dil}-04-A"
    ]
    df_etalon[f"Concentration étalon dilué {dil}"] = np.array(
        df_etalon["Concentration étalon (ppb)"][:5]
    ) * np.array(temp["Facteur de dilution"])

