import matplotlib.pyplot as plt
import numpy as np

from donnees_en_df import df_dil, df_blanc, df_InRe
from liste_elements import lis_name


x = df_blanc.loc["numérotation_blanc"].to_numpy()
for elem in lis_name[1:]:
    y = df_blanc.loc[elem].to_numpy()
    plt.scatter()
