import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from C1_donnees_en_df import df_InRe

print(df_InRe)
x = np.arange(0, 6, 1)
y1 = df_InRe.loc["115In"].to_numpy()
y2 = df_InRe.loc["185Re"].to_numpy()
plt.plot(x, y1, label="115In")
plt.plot(x, y2, label="185Re")
plt.xlabel("Nombre de coup de In/Re")
plt.ylabel("Essai")
plt.title("Mesure de dérive d'appareil")
plt.grid()
plt.legend()
plt.show()
