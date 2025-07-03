# Import des modules utiles
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

# Création des graphes
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

scatter_data = {}

# Boucle pour faire un graphe pour chaque élement
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

        # Régression initiale
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblancsensib[elt].append(coeffs)
        y_fit = np.polyval(coeffs, x)
        (line,) = ax.plot(x, y_fit, "--")
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

    # Met à jour la régression
    if len(x) > 1:
        coeffs = np.polyfit(x, y, 1)
        dico_elt_corblancsensib[elt][labels.index(scatter_data[sc]["label"])] = coeffs
        y_fit = np.polyval(coeffs, x)
        line = scatter_data[ax]["line"]
        line.set_data(x, y_fit)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("pick_event", onpick)
plt.show()
