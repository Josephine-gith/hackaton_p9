from donnees_en_df import df_dil
import pandas as pd

print(df_dil)

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_2025.xls")
df_factdil = pd.read_excel(xls, "indication_nom_echts", header=9)
df_factdil.drop(["Unnamed: 2", "Unnamed: 3"], axis=1, inplace=True)

df_etalon = pd.read_excel(xls, "solution-sdt_etalon", header=1)
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
    df_etalon[f"Concentration étalon dilué {dil}"] = (
        df_etalon["Concentration étalon (ppb)"] * (1 + dil)
        # * df_factdil[df_factdil['Standard étalon']==f"ET-DIL{dil}-04-A"]["Facteur de dilution"]
    )

print(df_etalon)
