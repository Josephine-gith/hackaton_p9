# Import des modules utiles
import matplotlib.pyplot as plt
import numpy as np

# Import des données
from C5_analyse_echlin_inc import df_concentration, df_incertitude

# Mise en forme du dataframe
df_incertitude.drop(
    ["numérotation_dilution", "numérotation_blanc", "numérotation_derive"], inplace=True
)

# Tracés pour la mesure SLRS5-AQ-1
x = np.array(df_concentration.index)[1:]
y = np.array(df_concentration.iloc[1:, 1])

plt.errorbar(x, y, yerr=y*np.array(df_incertitude.iloc[1:, 1]), fmt="o", ecolor="red")

plt.xlabel("Eléments")
plt.ylabel("Concentration (ppb)")
plt.title(f"Concentrations dans {np.array(df_concentration.loc["Sample"])[1]}")
plt.grid()

plt.show()
