# Import des modules utiles
import numpy as np
import matplotlib.pyplot as plt

# Import des données
from C1_donnees_en_df import df_dil, df_blanc, df_etalon, df_InRe
from C1_liste_elements import lis_name_clean

# liste des numéros de chaque mesure
labels = [
    "1ere mesures",
    "2eme mesures",
    "3eme mesures",
    "4eme mesures",
    "5eme mesures",
    "6eme mesures",
]
# Dictionnaire pour stocker les coefficients de régression linéaire
dico_elt_corblancsensib = {}

## Régression linéaire pour les éléments Na, Mg, Ca, Sr, Ba (tous sauf In et Re)

# Régression linéaire et stock des coefficients dans un dictionnaire
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

scatter_data = {}

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
        sc = ax.scatter(x, y, label=label, picker=True)
        scatter_data[sc] = {
            "x": list(x),
            "y": list(y),
            "ax": ax,
            "elt": elt,
            "label": label,
        }

        # Régression linéaire initiale
        coeffs = np.mean(y / x)
        dico_elt_corblancsensib[elt].append(coeffs)
        (line,) = ax.plot(x, coeffs * x, "--")
        scatter_data[ax] = {"line": line, "x": x, "y": y, "elt": elt}

    ax.set_title(elt)
    ax.grid()
    ax.legend()
fig.supylabel("Concentration (ppb)")
fig.supxlabel("Nombre de coût")


def onpick(event):
    sc = event.artist
    ind = event.ind[0]
    data = scatter_data[sc]
    x, y = data["x"], data["y"]
    ax = data["ax"]
    elt = data["elt"]

    # Supprime le point cliqué
    x.pop(ind)
    y.pop(ind)
    sc.set_offsets(np.c_[x, y])

    x, y = np.array(x), np.array(y)

    # Met à jour la régression
    if len(x) > 1:
        coeffs = np.mean(y / x)
        dico_elt_corblancsensib[elt][labels.index(scatter_data[sc]["label"])] = coeffs
        y_fit = coeffs * x
        line = scatter_data[ax]["line"]
        line.set_data(x, y_fit)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("pick_event", onpick)
plt.show()


## Régression linéaire pour les éléments In et Re

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Liste des éléments à traiter
elements = [("Re", "185Re"), ("In", "115In")]

scatter_data = {}

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
        indice_blanc = int(df_dil.loc["numérotation_blanc"].iloc[i_deb]) - 1
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
        sc = ax.scatter(x, y, label=label, picker=True)
        scatter_data[sc] = {
            "x": list(x),
            "y": list(y),
            "ax": ax,
            "elt": code_elt,
            "label": label,
        }

        # Régression linéaire
        coeffs = np.mean(y / x)
        dico_elt_corblancsensib[code_elt].append(coeffs)
        (line,) = ax.plot(x, coeffs * x, "--")
        scatter_data[ax] = {"line": line, "x": x, "y": y, "elt": code_elt}

    ax.set_title(nom_elt)
    ax.grid(True)
    ax.legend()

plt.tight_layout()

fig.supylabel("Concentration (ppb)")
fig.supxlabel("Nombre de coût")

fig.canvas.mpl_connect("pick_event", onpick)
plt.show()
