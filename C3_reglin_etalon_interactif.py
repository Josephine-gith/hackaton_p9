# Import des modules utiles
import numpy as np
import matplotlib.pyplot as plt

# Import des donnees
from C1_donnees_en_df import df_dil, df_etalon, df_InRe
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
dico_elt = {}

# Création des graphes
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

scatter_data = {}

# Boucle pour faire un graphe pour chaque élement
for idx, elt in enumerate(lis_name_clean):
    ax = axes[idx]
    dico_elt[elt] = []

    atome = "".join([c for c in elt if c.isalpha()])
    y = df_etalon.loc[atome].iloc[1:].to_numpy()
    y = np.array(y, dtype=float)

    for i, label in enumerate(labels):
        x = np.array(df_dil.loc[elt][i * 5 : (i + 1) * 5], dtype=float)
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
        dico_elt[elt].append(coeffs)
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
        dico_elt[elt][labels.index(scatter_data[sc]["label"])] = coeffs
        y_fit = np.polyval(coeffs, x)
        line = scatter_data[ax]["line"]
        line.set_data(x, y_fit)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("pick_event", onpick)

plt.show()


## Régression linéaire pour les éléments In et Re


# Régression linéaire et stock des coefficients dans un dictionnaire
fig, axes = plt.subplots(1, 2, figsize=(8, 4))

scatter_data = {}

for idx, elem in enumerate([("In", "115In"), ("Re", "185Re")]):
    ax = axes[idx]
    dico_elt[elem[1]] = []

    y = df_InRe[f"{elem[0]} (ppm)"].iloc[::-1].to_numpy()

    for i, label in enumerate(labels):
        x = np.array(df_dil.loc[elem[1]][i * 5 : (i + 1) * 5])
        x = np.array(x, dtype=float)
        sc = ax.scatter(x, y, label=label, picker=True)
        scatter_data[sc] = {
            "x": list(x),
            "y": list(y),
            "ax": ax,
            "elt": elem[1],
            "label": label,
        }

        # Régression linéaire numpy
        coeffs = np.polyfit(x, y, 1)
        dico_elt[elem[1]].append(coeffs)
        y_fit = np.polyval(coeffs, x)
        (line,) = ax.plot(x, y_fit, "--")
        scatter_data[ax] = {"line": line, "x": x, "y": y, "elt": elem[1]}

    ax.set_title(elem[0])
    ax.grid()
    ax.legend()
fig.supylabel("Concentration (ppm)")
fig.supxlabel("Nombre de coût")

fig.canvas.mpl_connect("pick_event", onpick)

plt.show()
