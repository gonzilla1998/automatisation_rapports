import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------------------------------------------------
# 1. Charger tous les CSV et créer des dataframes nommés
# ---------------------------------------------------------

loaded_names = []

folder_path = r"C:\Users\LoïcGonzalez\OneDrive - Airscan\4Externals - Documents\VEB - Ventilatie Audits\02. Project documents\4. Campaigns\To Do\Fifth batch\2. WZC Breugheldal\2. Data\Graph"

csv_files = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if f.lower().endswith(".csv")
]

globals_dict = globals()

for file in csv_files:
    df = pd.read_csv(file, sep=";", dtype=str)

    # Trouver colonnes CO2 et Date
    co2_col = next((c for c in df.columns if "CO2" in c), None)
    date_col = next((c for c in df.columns if "Date" in c), None)

    if co2_col is None or date_col is None:
        print(f"Skipping {os.path.basename(file)} — Date or CO2 col missing.")
        continue

    # Extraire colonnes d'intérêt
    df_selected = df[[date_col, co2_col]].copy()
    df_selected.columns = ["DateTimeStr", "CO2"]

    # Convertir CO2 (virgule → point)
    df_selected["CO2"] = df_selected["CO2"].str.replace(",", ".", regex=False)
    df_selected["CO2"] = pd.to_numeric(df_selected["CO2"], errors="coerce")

    # Nom de variable Python valide
    df_name = os.path.splitext(os.path.basename(file))[0].replace(" ", "_")

    globals_dict[df_name] = df_selected
    loaded_names.append(df_name)


# ---------------------------------------------------------
# 2. Fonction pour calculer les moyennes horaires
# ---------------------------------------------------------

def process_df(df):
    df = df.copy()

    # Conversion de la date (format R = dmy_hms)
    df["DateTime"] = pd.to_datetime(df["DateTimeStr"], dayfirst=True, errors="coerce")

    df["Date"] = df["DateTime"].dt.date
    df["Hour"] = df["DateTime"].dt.hour.astype(str).str.zfill(2) + ":00"

    hourly = (
        df.groupby(["Hour", "Date"])["CO2"]
        .mean()
        .reset_index()
        .pivot(index="Hour", columns="Date", values="CO2")
        .sort_index()
    )

    return hourly


# Créer les dataframes *_hourly
for name in loaded_names:
    df = globals_dict[name]
    hourly_df = process_df(df)
    globals_dict[f"{name}_hourly"] = hourly_df


# ---------------------------------------------------------
# 3. Fonction de plot
# ---------------------------------------------------------

def plot_hourly_df(df_hourly, title="CO₂ Concentrations"):
    df_long = df_hourly.reset_index().melt(id_vars="Hour", var_name="Date", value_name="CO2")

    # Convertir l'heure en datetime pour un axe correct
    df_long["Hour"] = pd.to_datetime(df_long["Hour"], format="%H:%M")

    plt.figure(figsize=(12, 6))

    for date in df_long["Date"].unique():
        subset = df_long[df_long["Date"] == date]
        plt.plot(subset["Hour"], subset["CO2"], label=str(date))

    plt.axhline(900, linestyle="--", color="darkgreen", linewidth=1.2)
    plt.axhline(1200, linestyle="--", color="red", linewidth=1.2)

    plt.title(title)
    plt.xlabel("Uren van de dag")
    plt.ylabel("CO₂ concentratie (ppm)")
    plt.legend(title="")
    plt.grid(True)
    plt.tight_layout()


# ---------------------------------------------------------
# 4. Export des graphes
# ---------------------------------------------------------

output_folder = r"C:\Users\LoïcGonzalez\OneDrive - Airscan\4Externals - Documents\VEB - Ventilatie Audits\02. Project documents\4. Campaigns\To Do\Fifth batch\1. Kinderdagverblijf Ons Huisje\2. Data\Graphs"
os.makedirs(output_folder, exist_ok=True)

for name in loaded_names:
    hourly_name = f"{name}_hourly"
    if hourly_name not in globals_dict:
        continue

    df = globals_dict[hourly_name]
    plot_hourly_df(df, title=hourly_name)

    out_path = os.path.join(output_folder, f"{hourly_name}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
