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
    y1 = y1 * 1000  # Conversion de ppm à ppb
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
        coeffs = np.mean(y/x)
        dico_elt_corblancsensib[elt].append(coeffs)
        ax.plot(
            x,
            coeffs*x,
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

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Liste des éléments à traiter
elements = [("Re", "185Re"), ("In", "115In")]

for idx, (nom_elt, code_elt) in enumerate(elements):
    ax = axes[idx]
    dico_elt_corblancsensib[code_elt] = []

    # y = concentration cible (en ppb)
    y = df_InRe[f"{nom_elt} (ppm)"].iloc[::-1].to_numpy() * 1000

    if code_elt == "185Re":
        # y1 = concentration en In (pour la correction)
        y1 = df_InRe["In (ppm)"].iloc[::-1].to_numpy() * 1000

    for i, label in enumerate(labels):
        # Plage des 5 dilutions
        i_deb, i_fin = i * 5, (i + 1) * 5

        # Récupération des données de dilution
        dilution = df_dil.loc[code_elt].iloc[i_deb:i_fin]
        indice_blanc = int(df_dil.loc['numérotation_blanc'].iloc[i_deb]) - 1
        valeur_blanc = df_blanc.loc[code_elt].iloc[indice_blanc]

        if code_elt == "185Re":
            # Correction In
            valeur_blancIn = df_blanc.loc["115In"].iloc[indice_blanc]
            x1 = df_dil.loc["115In"].iloc[i_deb:i_fin] - valeur_blancIn
            x = (dilution - valeur_blanc) / x1 * y1
        else:
            # Sans correction In
            x = dilution - valeur_blanc

        x = x.astype(float)
        ax.scatter(x, y, label=label)

        # Régression linéaire
        coeffs = np.mean(y/x)
        dico_elt_corblancsensib[code_elt].append(coeffs)
        ax.plot(x, coeffs*x, "--")

    ax.set_title(nom_elt)
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.show()



fig.supylabel("Concentration (ppb)")
fig.supxlabel("Nombre de coût")
plt.show()
