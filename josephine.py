import pandas as pd

xls = pd.ExcelFile('data/Fichier_donnees_ICP-MS_projets-Mines_2025.xls')
df = pd.read_excel(xls, 'resultats_bruts_ICP-MS')
#print(df.head())

df.dropna(axis=1, how='any', inplace=True)

df = df[df['File:'].isin(['Sample','Na / 23 [#3]'])].reset_index(drop=True)

print(df.head())
