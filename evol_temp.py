# Import des modules utiles
import matplotlib.pyplot as plt
import numpy as np

# Import des données
from donnees_en_df import df_dil, df_blanc, df_InRe
from liste_elements import lis_name

## Tracé des concentrations dans les blancs et les échantillons InRe au cours des expériences

for sample, df in [('blancs', df_blanc), ('échantillons InRe', df_InRe)]:
    fig, axes = plt.subplots(2, 1)
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
    #plt.show()

## Tracé des concentrations dans échantillons standards au cours des expériences

fig, axes = plt.subplots(2,3)
axes.flatten()


i = 0
for e in df_dil.loc["numérotation_dilution"].to_numpy():
    if e % 1 == i:
        y.append(df_dil[])

for 