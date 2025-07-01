import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from donnees_en_df import df_dil

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_2025.xls")
df_InRe = pd.read_excel(xls, "solution-sdt_InRe", header=6)

for elem in ['In', 'Re']:

    x = df_InRe[f"{elem} (ppm)"].iloc[::-1].to_numpy()

    labels = [
        "1ere mesures",
        "2eme mesures",
        "3eme mesures",
        "4eme mesures",
        "5eme mesures",
        "6eme mesures",
    ]

for i, label in enumerate(labels):
    y = np.array(df_dil.loc["115In"][i * 5 : (i + 1) * 5])
    y = np.array(y, dtype=float)
    print(y, y.dtype)
    plt.plot(x, y, label=label)
    # Régression linéaire numpy
    coeffs = np.polyfit(x, y, 1)
    y_fit = np.polyval(coeffs, x)
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
