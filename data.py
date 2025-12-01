import os
import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Load all CSV files
# -----------------------------

folder_path = "C:/Users/LoïcGonzalez/OneDrive - Airscan/4Externals - Documents/VEB - Ventilatie Audits/02. Project documents/4. Campaigns/To Do/Fifth batch/2. WZC Breugheldal/2. Data/CSV/Cleaned"
def load_csv_files(folder_path):
    loaded_names = []    # ÉQUIVALENT R : vector storing object names
    globals_dict = {}    # ÉQUIVALENT R : environment to store created dataframes

    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

    for file in csv_files:
        full_path = os.path.join(folder_path, file)

        # Read CSV like read.csv2 (semicolon + comma decimal)
        df = pd.read_csv(full_path, sep=';', dtype=str)

        # Equivalent of grep("CO2")
        co2_cols = [c for c in df.columns if "CO2" in c]
        date_cols = [c for c in df.columns if "Date" in c]

        if not co2_cols or not date_cols:
            print(f"Skipping {file} - Date or CO2 column not found.")
            continue

        co2_col = co2_cols[0]
        date_col = date_cols[0]

        # Extract columns
        df_sel = df[[date_col, co2_col]].copy()
        df_sel.columns = ["DateTimeStr", "CO2"]

        # Convert CO2 values (comma decimal)
        df_sel["CO2"] = df_sel["CO2"].str.replace(",", ".", regex=False).astype(float)

        # Make safe variable name like in R
        df_name = os.path.splitext(file)[0].replace(" ", "_")

        # assign(df_name, df_sel)
        globals_dict[df_name] = df_sel

        loaded_names.append(df_name)

    # -----------------------------
    # 2. Compute statistics
    # -----------------------------

    import numpy as np

    summary_rows = []

    for name in loaded_names:
        df = globals_dict[name]

        # Parse datetime like dmy_hms()
        df["DateTime"] = pd.to_datetime(df["DateTimeStr"], errors="coerce", dayfirst=True)

        df["Hour"] = df["DateTime"].dt.hour + df["DateTime"].dt.minute / 60
        df["Day"] = df["DateTime"].dt.weekday
        df["Weekday"] = df["Day"].between(0, 4)
        df["Operational"] = (
        df["Weekday"]
        & (df["Hour"] >= 9.5)
        & (df["Hour"] < 19.5)
    )

        # ALL DATA
        mean_all = df["CO2"].mean()
        min_all = df["CO2"].min()
        max_all = df["CO2"].max()
        pct_900_all = (df["CO2"] > 900).mean() * 100
        pct_1200_all = (df["CO2"] > 1200).mean() * 100

        # OPERATIONAL HOURS
        df_op = df[df["Operational"]]

        mean_op = df_op["CO2"].mean()
        min_op = df_op["CO2"].min()
        max_op = df_op["CO2"].max()
        pct_900_op = (df_op["CO2"] > 900).mean() * 100
        pct_1200_op = (df_op["CO2"] > 1200).mean() * 100

        summary_rows.append({
            "Device": name,
            "Mean_All": mean_all,
            "Min_All": min_all,
            "Max_All": max_all,
            "Percent_Above_900_All": pct_900_all,
            "Percent_Above_1200_All": pct_1200_all,
            "Mean_Op": mean_op,
            "Min_Op": min_op,
            "Max_Op": max_op,
            "Percent_Above_900_Op": pct_900_op,
            "Percent_Above_1200_Op": pct_1200_op
        })

    summary_stats = pd.DataFrame(summary_rows)
    print(summary_stats)
    return summary_stats

summary_stats=load_csv_files(folder_path)
# -----------------------------
# 3. Export to CSV
# -----------------------------

output_folder = r"C:\Users\LoïcGonzalez\OneDrive - Airscan\4Externals - Documents\VEB - Ventilatie Audits\02. Project documents\4. Campaigns\To Do\Fifth batch\2. WZC Breugheldal\2. Data"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, "CO2_summary_stats.csv")
summary_stats.to_csv(output_file, index=False)

print(f"\nCSV successfully saved to:\n{output_file}\n")
