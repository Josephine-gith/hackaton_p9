# Import des modules utiles
import matplotlib.pyplot as plt
import numpy as np

# Import des données
from C1_donnees_en_df import df_dil, df_blanc, df_derive, liste_dil
from C1_liste_elements import lis_name

## Tracé des concentrations dans les blancs et les échantillons InRe au cours des expériences


for sample, df, numerotation in [
    ("blancs", df_blanc, "numérotation_blanc"),
    ("échantillons InRe", df_derive, "numérotation_derive"),
]:
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    x = df.loc[numerotation].to_numpy()

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

fig, axes = plt.subplots(1, len(liste_dil), figsize=(10, 3))

nb_serie_dilution = df_dil.loc['Sample'].value_counts().iloc[0]

y = np.zeros([len(liste_dil), nb_serie_dilution, len(lis_name[1:])])
x = np.arange(1, nb_serie_dilution+1)

lis_dil = [0 for _ in range(len(liste_dil))]
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

handles, labels = axes[0].get_legend_handles_labels()

fig.suptitle("Nombre de coût dans les standards au cours des expériences")
fig.supylabel("nombre de coût")
fig.tight_layout(rect=(0, 0, 0.85, 1))
plt.legend(handles, labels, loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()