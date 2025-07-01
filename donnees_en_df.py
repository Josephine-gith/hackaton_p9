# Import de modules utiles
import pandas as pd

# Import des données
from liste_elements import lis_index, lis_name

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
df_InRe = df.loc[:, df.loc["Sample"] == "InRe-A"]
# mesures de l'expérience
df_ech_intermediaire1 = df.drop(columns=df_dil.columns)
df_ech_intermediaire2 = df_ech_intermediaire1.drop(columns=df_blanc.columns)
df_ech = df_ech_intermediaire2.drop(columns=df_InRe.columns)
