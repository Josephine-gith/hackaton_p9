import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from donnees_en_df import df_dil
from liste_elements import lis_index_2, lis_name_clean

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_20252.xls")

labels = [
    "1ere mesures",
    "2eme mesures",
    "3eme mesures",
    "4eme mesures",
    "5eme mesures",
    "6eme mesures",
]
dico_elt = {}

df_facteur_dilution = pd.read_excel(xls, "indication_nom_echts", header=9)
df_facteur_dilution.drop(["Unnamed: 2", "Unnamed: 3"], axis=1, inplace=True)
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
for dil in [100, 30, 10, 3, 0]:
    temp = df_facteur_dilution[
        df_facteur_dilution["Standard étalon"] == f"ET-DIL{dil}-04-A"
    ]
    df_etalon[f"Concentration étalon dilué {dil}"] = np.array(
        df_etalon["Concentration étalon (ppb)"][:5]
    ) * np.array(temp["Facteur de dilution"])



# Graphes 

fig, axes = plt.subplots(1,1)

# On stocke les données pour chaque scatter
scatter_data = {}

elt = "23Na"
ax = axes
dico_elt[elt] = []

atome = "".join([c for c in elt if c.isalpha()])
y = df_etalon.loc[atome].iloc[1:].to_numpy()
y = np.array(y, dtype=float)

i = 0
label = labels[i]
x = np.array(df_dil.loc[elt][i * 5 : (i + 1) * 5], dtype=float)
sc = ax.scatter(x, y, label=label, picker=True)
# On stocke les coordonnées et l'objet scatter
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
(line,) = ax.plot(x, y_fit, "--", color="red")
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
        y_fit = np.polyval(coeffs, x)
        line = scatter_data[ax]["line"]
        line.set_data(x, y_fit)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("pick_event", onpick)
plt.show()
