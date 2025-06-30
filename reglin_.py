import matplotlib.pyplot as plt
import pandas as pd

from donnees_en_df import df

xls = pd.ExcelFile("data/Fichier_traitement_donnees_ICP-MS_projets-Mines_2025.xls")
df_InRe = pd.read_excel(xls, "solution-sdt_InRe", header=6)

plt.plot(df_InRe['In (ppm)'], df.loc[['115In'], ['ET-DIL0-04-A','ET-DIL3-04-A','ET-DIL10-04-A','ET-DIL30-04-A','ET-DIL100-04-A']])
plt.show()
