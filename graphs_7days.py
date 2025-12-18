import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize


df = pd.read_csv("Data/Data_cleaned/Cafetaria.csv", sep=";")

df = df.rename(columns={"Date": "time", "CO2(ppm)": "CO2"})
# df doit contenir: df["time"] (datetime) et df["CO2"] (ppm)
# df["time"] = pd.to_datetime(df["time"])

t = df["time"].to_numpy()
y = df["CO2"].to_numpy()

# --- Couleurs bande CO2 (vert -> jaune -> rouge)
vmin, vmax = 900, 1200
norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
cmap = LinearSegmentedColormap.from_list("co2_scale", ["#6CC04A", "#F2D24B", "#E5534B"])

x = mdates.date2num(pd.to_datetime(t))

fig, (ax, ax_bar) = plt.subplots(
    2, 1, figsize=(12, 4.2), sharex=True,
    gridspec_kw={"height_ratios": [5, 0.7], "hspace": 0.05}
)

# =========================
# 1) Bandes "pièce ouverte" (fond)
# =========================
# ---- OPTION A: si df["open"] existe (bool)
if "open" in df.columns:
    open_mask = df["open"].fillna(False).to_numpy().astype(bool)

    # On détecte les segments True consécutifs et on fait des axvspan
    idx = np.flatnonzero(open_mask)
    if idx.size > 0:
        # regroupe les indices contigus
        splits = np.where(np.diff(idx) > 1)[0] + 1
        groups = np.split(idx, splits)
        for g in groups:
            start_i, end_i = g[0], g[-1]
            # end_i+1 pour couvrir jusqu’au point suivant si possible
            x0 = x[start_i]
            x1 = x[end_i + 1] if end_i + 1 < len(x) else x[end_i]
            ax.axvspan(x0, x1, alpha=0.10)  # bandes un peu sombres

# ---- OPTION B: horaires fixes (ex: 08:00–18:00 lun-ven)
# (Décommente si tu n’as pas df["open"])
# open_start = "08:00"
# open_end   = "18:00"
# days = pd.to_datetime(df["time"]).dt.floor("D").unique()
# for d in days:
#     d = pd.Timestamp(d)
#     if d.weekday() < 5:  # 0=lun ... 4=ven
#         x0 = mdates.date2num(pd.Timestamp(f"{d.date()} {open_start}"))
#         x1 = mdates.date2num(pd.Timestamp(f"{d.date()} {open_end}"))
#         ax.axvspan(x0, x1, alpha=0.10)

# =========================
# 2) Courbe noire
# =========================
ax.plot(pd.to_datetime(t), y, color="black", linewidth=1.0)
ax.set_ylabel("ppm")
ax.grid(True, alpha=0.25)
ax.set_title("CO2", loc="left", fontweight="bold")

# =========================
# 3) Bande colorée en bas (selon CO2)
# =========================
# segments horizontaux entre chaque paire de timestamps
bar_segs = np.array([[[x[i], 0], [x[i+1], 0]] for i in range(len(x)-1)], dtype=float)
bar_lc = LineCollection(bar_segs, cmap=cmap, norm=norm, linewidth=10, capstyle="butt")
bar_lc.set_array((y[:-1] + y[1:]) / 2)
ax_bar.add_collection(bar_lc)

ax_bar.set_ylim(-1, 1)
ax_bar.set_yticks([])
for spine in ["left", "right", "top"]:
    ax_bar.spines[spine].set_visible(False)

# Axe temps
ax_bar.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=12))
ax_bar.xaxis.set_major_formatter(mdates.DateFormatter("%a %d\n%H:%M"))

plt.show()
