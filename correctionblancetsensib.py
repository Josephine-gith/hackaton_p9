# Import des modules utiles
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import des données
from donnees_en_df import df_dil, df_blanc, df_etalon, df_InRe
from liste_elements import lis_name_clean

# Variables globales
labels = [
    "1ere mesures",
    "2eme mesures",
    "3eme mesures",
    "4eme mesures",
    "5eme mesures",
    "6eme mesures",
]
dico_elt_corblancsensib = {}

## Régression linéaire pour les éléments Na, Mg, Ca, Sr, Ba (tous sauf In et Re)

# Régression linéaire et stock des coefficients dans un dictionnaire
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for idx, elt in enumerate(lis_name_clean):
    ax = axes[idx]
    dico_elt_corblancsensib[elt] = []

    atome = "".join([c for c in elt if c.isalpha()])
    y = df_etalon.loc[atome].iloc[1:].to_numpy()
    y1 = df_InRe["In (ppm)"].iloc[::-1].to_numpy()
    y = np.array(y, dtype=float)

    for i, label in enumerate(labels):
        ligne = df_dil.loc[elt]
        indice_blanc = int(np.array(df_dil.loc["numérotation_blanc"])[i * 5] - 1)
        valeur_blanc = np.array(df_blanc.loc[elt])[indice_blanc]
        valeur_blancIn = np.array(df_blanc.loc["115In"])[indice_blanc]
        # On soustrait la valeur du blanc pour chaque élément
        # pour obtenir la concentration corrigée
        x = np.array(ligne[i * 5 : (i + 1) * 5] - valeur_blanc)
        x1 = np.array(df_dil.loc["115In"][i * 5 : (i + 1) * 5] - valeur_blancIn)

        x = np.array((x / x1) * y1, dtype=float)
        ax.scatter(x, y, label=label)

        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblancsensib[elt].append(coeffs)
        y_fit = np.polyval(coeffs, x)
        ax.plot(
            x,
            y_fit,
            "--",
            # label=f"(a={coeffs[0]:.2e}, b={coeffs[1]:.2e})",
        )

    ax.set_title(elt)
    ax.grid()
    ax.legend()
fig.supylabel("Concentration (ppb)")
fig.supxlabel("Nombre de coût")
plt.show()


## Régression linéaire pour les éléments In et Re

# Régression linéaire et stock des coefficients dans un dictionnaire
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
for idx, elt in enumerate([("In", "115In"), ("Re", "185Re")]):
    ax = axes[idx]
    dico_elt_corblancsensib[elt[1]] = []

    y = df_InRe[f"{elt[0]} (ppm)"].iloc[::-1].to_numpy()

    for i, label in enumerate(labels):
        ligne = df_dil.loc[elt[1]]
        indice_blanc = int(np.array(df_dil.loc["numérotation_blanc"])[i * 5] - 1)
        valeur_blanc = np.array(df_blanc.loc[elt[1]])[indice_blanc]
        x = np.array(df_dil.loc[elt[1]][i * 5 : (i + 1) * 5] - valeur_blanc)
        x = np.array(x, dtype=float)
        ax.scatter(x, y, label=label)

        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblancsensib[elt[1]].append(coeffs)
        y_fit = np.polyval(coeffs, x)
        ax.plot(
            x,
            y_fit,
            "--",
            # label=f"(a={coeffs[0]:.2e}, b={coeffs[1]:.2e})",
        )

    ax.set_title(elt[0])
    ax.grid()
    ax.legend()
fig.supylabel("Concentration (ppm)")
fig.supxlabel("Nombre de coût")
plt.show()
