# Import des modules utiles
import matplotlib.pyplot as plt
import numpy as np

# Import des données
from donnees_en_df import df_dil, df_blanc, df_InRe
from liste_elements import lis_name

## Tracé des concentrations dans les blancs et les échantillons InRe au cours des expériences

for sample, df in [("blancs", df_blanc), ("échantillons InRe", df_InRe)]:
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    x = df.loc["numérotation_blanc"].to_numpy()

    for elem in lis_name[2:]:
        y = df.loc[elem].to_numpy()
        axes[0].plot(x, y, "+-", label=elem)
        axes[1].plot(x, y, "+-")

    # La concentration de Na étant beaucoup plus grande
    # on trace le graphe avec et sans pour bien voir les évolutions des autres éléments
    y = df.loc[lis_name[1]].to_numpy()
    axes[0].plot(x, y, "+-", label=lis_name[1])

    fig.supylabel("Nombre de coûts")
    fig.supxlabel("numéro de la mesure")
    fig.suptitle(f"Nombre de coûts dans les {sample} au cours des expériences")
    fig.legend()
    axes[0].grid()
    axes[1].grid()

## Tracé des concentrations dans échantillons standards au cours des expériences

fig, axes = plt.subplots(1, 5, figsize=(10, 2))
axes.flatten()

y = np.zeros([5, 6, len(lis_name[1:])])
x = np.arange(1, 7)

lis_dil = [0 for _ in range(5)]
for col in df_dil.columns:
    dil = round((df_dil[col].loc["numérotation_dilution"] % 1) * 100)
    num_exp = int(df_dil[col].loc["numérotation_dilution"])
    y[dil][num_exp - 1] = df_dil[col][1:-3]
    lis_dil[dil] = df_dil[col].loc["Sample"]

for i_dil, dil in enumerate(lis_dil):
    for i_elem in range(len(lis_name[1:])):
        axes[i_dil].plot(x, y[i_dil, :, i_elem], "+-", label=lis_name[i_elem + 1])
        axes[i_dil].grid()
        axes[i_dil].set_xlabel(dil)


fig.suptitle("Nombre de coût dans les standards au cours des expériences")
fig.supylabel("nombre de coût")
axes[0].legend()
plt.show()
