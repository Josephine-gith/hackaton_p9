import pandas as pd
from listeindex import lis_index, lis_name

xls = pd.ExcelFile("data/Fichier_donnees_ICP-MS_projets-Mines_2025.xls")
df = pd.read_excel(xls, "resultats_bruts_ICP-MS")

# Selection des données du DataFrame intéressantes
df.dropna(axis=1, how="any", inplace=True)
df = df[df["File:"].isin(lis_index)].reset_index(drop=True)

# Changement d'indexation
df["File:"] = lis_name
df.set_index(df["File:"], inplace=True)
df.drop("File:", axis=1, inplace=True)

print(df)
