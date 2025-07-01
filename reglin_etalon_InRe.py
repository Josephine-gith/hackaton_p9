import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from donnees_en_df import df_dil
from reglin_etalon import dico_elt

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_2025.xls")
df_InRe = pd.read_excel(xls, "solution-sdt_InRe", header=6)

plt.figure()
for elem in [('In', '115In', 1), ('Re','185Re', 2)]:
    plt.subplot(2,1,elem[2])

    y = df_InRe[f"{elem[0]} (ppm)"].iloc[::-1].to_numpy()

    labels = [
        "1ere mesures",
        "2eme mesures",
        "3eme mesures",
        "4eme mesures",
        "5eme mesures",
        "6eme mesures",
    ]

    dico_elt[elem[1]] = []

    for i, label in enumerate(labels):
        x = np.array(df_dil.loc[elem[1]][i * 5 : (i + 1) * 5])
        x = np.array(x, dtype=float)
        plt.scatter(x, y, label=label)
        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        y_fit = np.polyval(coeffs, x)
        plt.plot(
            x,
            y_fit,
            "--",
            # label=f"(a={coeffs[0]:.2e}, b={coeffs[1]:.2e})",
        )
        dico_elt[elem[1]].append(coeffs)

    plt.tick_params('x', labelbottom=(elem[2]!=1))
    plt.ylabel(f"Concentration de {elem[0]} en ppm")
    plt.title(f"Etalons pour {elem[0]}")
    plt.grid()
    plt.legend()
plt.xlabel("Nombre de coût")
plt.show()