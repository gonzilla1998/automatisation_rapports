import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from data import csv_download

# ---------------------------------------------------------
# 1. Charger tous les CSV et créer des dataframes nommés
# ---------------------------------------------------------y


# ---------------------------------------------------------
# 2. Fonction pour calculer les moyennes horaires
# ---------------------------------------------------------

def process_df(df):
    df = df.copy()

    # Conversion de la date (format R = dmy_hms)
    df["DateTime"] = pd.to_datetime(df["DateTimeStr"],  errors="coerce",dayfirst=True)

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



# ---------------------------------------------------------
# 3. Fonction de plot
# ---------------------------------------------------------

def plot_hourly_df(df_hourly):
    


    df_long = df_hourly.reset_index().melt(id_vars="Hour", var_name="Date", value_name="CO2")

    # Convertir l'heure en datetime pour un axe correct
    df_long["Hour"] = pd.to_datetime(df_long["Hour"], format="%H:%M")

    plt.figure(figsize=(12, 6))

    for date in df_long["Date"].unique():
        subset = df_long[df_long["Date"] == date]
        plt.plot(subset["Hour"], subset["CO2"], label=str(date))

    plt.axhline(900, linestyle="--", color="darkgreen", linewidth=1.2)
    plt.axhline(1200, linestyle="--", color="red", linewidth=1.2)

    
    plt.xlabel("Uren van de dag")
    plt.ylabel("CO₂ concentratie (ppm)")
    plt.legend(title="")
    plt.grid(True)
    plt.tight_layout()



# ---------------------------------------------------------
# 4. Export des graphes
# ---------------------------------------------------------

def export_graphs(folder_path, output_folder):
    loaded_names, globals_dict = csv_download(folder_path)

    for name in loaded_names:
        df = globals_dict[name]
        hourly_df = process_df(df)
        globals_dict[f"{name}_hourly"] = hourly_df
    graph_folder = os.path.join(output_folder, "Graphs")
    os.makedirs(graph_folder, exist_ok=True)

    for name in loaded_names:
        hourly_name = f"{name}_hourly"
        if hourly_name not in globals_dict:
            continue

        df = globals_dict[hourly_name]
        plot_hourly_df(df)

        out_path = os.path.join(graph_folder, f"{hourly_name}.png")
        plt.savefig(out_path, dpi=300)
        plt.close()

  
