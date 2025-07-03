# Import des modules utiles
import numpy as np
import matplotlib.pyplot as plt

# Import des données
from C1_donnees_en_df import df_dil, df_blanc, df_InRe, df_etalon
from C1_liste_elements import lis_name_clean


# Variables globales
labels = [
    "1ere mesures",
    "2eme mesures",
    "3eme mesures",
    "4eme mesures",
    "5eme mesures",
    "6eme mesures",
]
dico_elt_corblanc = {}

## Régression linéaire pour les éléments Na, Mg, Ca, Sr, Ba (tous sauf In et Re)

# Régression linéaire et stock des coefficients dans un dictionnaire
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for idx, elt in enumerate(lis_name_clean):
    ax = axes[idx]
    dico_elt_corblanc[elt] = []

    atome = "".join([c for c in elt if c.isalpha()])
    y = df_etalon.loc[atome].iloc[1:].to_numpy()
    y = np.array(y, dtype=float)

    for i, label in enumerate(labels):
        ligne = df_dil.loc[elt]
        indice_blanc = int(np.array(df_dil.loc["numérotation_blanc"])[i * 5] - 1)
        valeur_blanc = np.array(df_blanc.loc[elt])[indice_blanc]

        x = np.array(ligne[i * 5 : (i + 1) * 5] - valeur_blanc)

        x = np.array(x, dtype=float)
        ax.scatter(x, y, label=label)

        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblanc[elt].append(coeffs)
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
    dico_elt_corblanc[elt[1]] = []

    y = df_InRe[f"{elt[0]} (ppm)"].iloc[::-1].to_numpy()
    y = y * 1000  # Conversion de ppm à ppb
    for i, label in enumerate(labels):
        ligne = df_dil.loc[elt[1]]
        indice_blanc = int(np.array(df_dil.loc["numérotation_blanc"])[i * 5] - 1)
        valeur_blanc = np.array(df_blanc.loc[elt[1]])[indice_blanc]
        x = np.array(df_dil.loc[elt[1]][i * 5 : (i + 1) * 5] - valeur_blanc)
        x = np.array(x, dtype=float)
        ax.scatter(x, y, label=label)

        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblanc[elt[1]].append(coeffs)
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
fig.supylabel("Concentration (ppb)")
fig.supxlabel("Nombre de coût")
plt.show()
print(dico_elt_corblanc)
