from donnees_en_df import df_dil
from liste_elements import lis_index_2, lis_name_clean
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("a")
xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_20252.xls")
df_factdil = pd.read_excel(xls, "indication_nom_echts", header=9)
df_factdil.drop(["Unnamed: 2", "Unnamed: 3"], axis=1, inplace=True)

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

for dil in [0, 3, 10, 30, 100]:
    temp = df_factdil[df_factdil["Standard étalon"] == f"ET-DIL{dil}-04-A"]
    df_etalon[f"Concentration étalon dilué {dil}"] = np.array(
        df_etalon["Concentration étalon (ppb)"][:5]
    ) * np.array(temp["Facteur de dilution"])

print(df_etalon.index)

labels = [
    "1ere mesures",
    "2eme mesures",
    "3eme mesures",
    "4eme mesures",
    "5eme mesures",
    "6eme mesures",
]
dico_elt = {}
for elt in lis_name_clean:
    coefficients = []
    atome = "".join([c for c in elt if c.isalpha()])
    x = df_etalon.loc[atome].iloc[1:].to_numpy()
    x = np.array(x, dtype=float)
    print(x, x.dtype, x[0].dtype)
    for i, label in enumerate(labels):
        y = np.array(df_dil.loc[elt][i * 5 : (i + 1) * 5])
        y = np.array(y, dtype=float)
        print(y, y.dtype)
        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        coefficients.append(coeffs)
    dico_elt[elt] = coefficients
    """y_fit = np.polyval(coeffs, x)
    plt.plot(
        x,
        y_fit,
        "--",
        # label=f"(a={coeffs[0]:.2e}, b={coeffs[1]:.2e})",
    )

    plt.xlabel("Concentration de In en ppm")
    plt.ylabel("Nombre de coût")
    plt.title("Etalons pour In")
    plt.grid()
    plt.legend()
    plt.show()

#print(df_etalon.columns)"""
print(dico_elt)
