import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.colors as mcolors
import datetime
import numpy as np
# --- Configuration ---
CSV_PATH = r'C:\pyprojects\VEB_report_automation\Data\Data_cleaned\Kamer 96.csv'
OUTPUT_PATH = r'co2_graph.png'
# Colors
COLOR_CO2_LINE = 'black'
COLOR_GRID_MAJOR = '#d9d9d9'
COLOR_GRID_MINOR = '#e6e6e6'
COLOR_LOW = '#8bc34a'   # Green < 900
COLOR_MED = '#ffeb3b'   # Yellow/Orange 900-1200
COLOR_HIGH = '#f44336'  # Red > 1200
def load_data(filepath):
    """Loads and preprocesses the CSV data."""
    try:
        df = pd.read_csv(filepath, sep=';')
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S')
        df = df.sort_values('Date')
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
def get_co2_color(value):
    if value < 900:
        return COLOR_LOW
    elif value < 1200:
        return COLOR_MED
    else:
        return COLOR_HIGH
def smart_date_formatter(x, pos=None):
    """
    Formats the tick label based on the time.
    If it's midnight (00:00), show 'Day Date' (e.g. Wed 03).
    Otherwise, show 'HH:00'.
    """
    dt = mdates.num2date(x)
    # Check if hour is 0 (approximate due to floats)
    # We can check if the time is close to midnight
    if dt.hour == 0 and dt.minute == 0:
        return dt.strftime('%a %d')
    else:
        return dt.strftime('%H:00')
def plot_co2_graph(df, schedule=None):
    """Generates the CO2 graph with side summary.
    
    Args:
        df: DataFrame with CO2 data
        schedule: Dict mapping weekday (0=Mon, 6=Sun) to (open_hour, open_min, close_hour, close_min).
                  Example: {0: (8, 30, 19, 30), 1: (9, 0, 17, 0)}
                  Days not in dict are considered closed.
                  Default: Mon-Fri 8:30-19:30
    """
    # Default schedule: Monday to Friday, 8:30-19:30
    if schedule is None:
        schedule = {
            0: (8, 30, 19, 30),  # Monday
            1: (8, 30, 19, 30),  # Tuesday
            2: (8, 30, 19, 30),  # Wednesday
            3: (8, 30, 19, 30),  # Thursday
            4: (8, 30, 19, 30),  # Friday
            5: (8, 30, 19, 30),
            6: (8, 30, 19, 30),
        }
    
    if df is None or df.empty:
        print("No data to plot.")
        return
    # Use Full Data
    plot_data = df.copy()
    # --- Setup Figure & GridSpec ---
    # Width ratio: 1 (Summary) : 4 (Graph Area)
    # Height ratio: Graph (Big), Strip (Thin), Spacer/Ruler (Medium)
    # User requested: "Moins haute et plus large" (Less tall, wider)
    fig = plt.figure(figsize=(18, 5))
    
    # GridSpec: 3 Rows for the right side
    # Row 0: Main Graph
    # Row 1: Color Strip (Attached to Graph)
    # Row 2: Ruler/Axis (Separated)
    # Using 4 rows logic: Graph, Strip, Spacer, Ruler.
    gs = GridSpec(4, 2, width_ratios=[1, 4], height_ratios=[8, 0.5, 0.5, 1.0], wspace=0.08, hspace=0.0)
    # Ax1: Summary Panel (Spanning all rows on the left)
    ax_summary = fig.add_subplot(gs[:, 0])
    ax_summary.axis('off')
    
    # Ax2: Top Graph (CO2 Line) - Row 0
    ax_graph = fig.add_subplot(gs[0, 1])
    
    # Ax3: Bottom Graph (Color Strip) - Row 1
    # Share X with graph to stay aligned
    ax_strip = fig.add_subplot(gs[1, 1], sharex=ax_graph)
    
    # Ax4: Ruler (Ticks) - Row 3 (Skipping Row 2 which is spacer)
    ax_ruler = fig.add_subplot(gs[3, 1], sharex=ax_graph)
    # --- Calculation: Average on Opening Hours Only ---
    def is_open(row):
        """Check if a given datetime is during opening hours"""
        weekday = row['Date'].weekday()
        if weekday not in schedule:
            return False
        open_h, open_m, close_h, close_m = schedule[weekday]
        time_val = row['Date'].time()
        return datetime.time(open_h, open_m) <= time_val <= datetime.time(close_h, close_m)
    
    open_mask = plot_data.apply(is_open, axis=1)
    
    if open_mask.any():
        avg_ppm = plot_data.loc[open_mask, 'CO2(ppm)'].mean()
    else:
        avg_ppm = plot_data['CO2(ppm)'].mean()
    indicator_color = get_co2_color(avg_ppm)
    # --- Draw Summary Panel (Left) ---
    ax_summary.text(0.1, 0.95, "CO2", fontsize=18, fontweight='bold', transform=ax_summary.transAxes)
    
    # Legend
    ax_summary.add_patch(plt.Rectangle((0.1, 0.88), 0.25, 0.03, color=COLOR_LOW, transform=ax_summary.transAxes, clip_on=False))
    ax_summary.add_patch(plt.Rectangle((0.35, 0.88), 0.25, 0.03, color=COLOR_MED, transform=ax_summary.transAxes, clip_on=False))
    ax_summary.add_patch(plt.Rectangle((0.60, 0.88), 0.25, 0.03, color=COLOR_HIGH, transform=ax_summary.transAxes, clip_on=False))
    
    ax_summary.text(0.1, 0.85, "900", fontsize=8, ha='left', transform=ax_summary.transAxes)
    ax_summary.text(0.60, 0.85, "1200", fontsize=8, ha='center', transform=ax_summary.transAxes)
    ax_summary.text(0.85, 0.85, "ppm", fontsize=8, ha='left', transform=ax_summary.transAxes)
    # Indicator
    rect = plt.Rectangle((0.15, 0.45), 0.7, 0.25, facecolor=indicator_color, edgecolor='none', 
                         transform=ax_summary.transAxes, zorder=1)
    ax_summary.add_patch(rect)
    
    ax_summary.text(0.5, 0.60, f"{int(avg_ppm)}", fontsize=24, fontweight='bold', ha='center', va='center', 
                    transform=ax_summary.transAxes, color='black', zorder=2)
    ax_summary.text(0.5, 0.52, "ppm", fontsize=16, ha='center', va='center', 
                    transform=ax_summary.transAxes, color='black', zorder=2)
    # Text near ruler
    ax_summary.text(0.95, 0.05, "Period of presence:", fontsize=10, fontweight='bold', ha='right', va='bottom', 
                    transform=ax_summary.transAxes)
    # --- Draw Top Graph (Right) ---
    ax_graph.plot(plot_data['Date'], plot_data['CO2(ppm)'], color=COLOR_CO2_LINE, linewidth=1, zorder=10)
    
    x_min = plot_data['Date'].min()
    x_max = plot_data['Date'].max()
    ax_graph.set_xlim(x_min, x_max)
    
    ax_graph.set_ylim(0, max(800, plot_data['CO2(ppm)'].max() * 1.1))
    ax_graph.set_ylabel("ppm", fontsize=10)
    # Create grid that divides day in 3 (00, 08, 16)
    ax_graph.xaxis.set_major_locator(mdates.DayLocator())
    ax_graph.xaxis.set_minor_locator(mdates.HourLocator(byhour=[8, 16]))
    
    ax_graph.grid(True, which='major', axis='x', color='#333333', linestyle='-', linewidth=1, alpha=0.3)
    ax_graph.grid(True, which='minor', axis='x', color='#888888', linestyle='-', linewidth=0.5, alpha=0.3)
    ax_graph.grid(True, axis='y', color=COLOR_GRID_MINOR, linestyle='-', linewidth=0.5) 
    
    plt.setp(ax_graph.get_xticklabels(which='both'), visible=False)
    ax_graph.tick_params(axis='x', which='both', length=0) 
    # --- Shading Opening Hours ---
    current_day = x_min.replace(hour=0, minute=0, second=0, microsecond=0)
    end_plot_day = x_max.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    
    while current_day < end_plot_day:
        weekday = current_day.weekday()
        if weekday in schedule:
            open_h, open_m, close_h, close_m = schedule[weekday]
            opening_time = current_day + datetime.timedelta(hours=open_h, minutes=open_m)
            closing_time = current_day + datetime.timedelta(hours=close_h, minutes=close_m)
            ax_graph.axvspan(opening_time, closing_time, facecolor='#eef5f9', alpha=1.0, zorder=0) 
        current_day += datetime.timedelta(days=1)
    # --- Draw Bottom Strip (Right) ---
    dates = mdates.date2num(plot_data['Date'])
    if len(dates) > 1:
        width = np.mean(np.diff(dates))
    else:
        width = 1/(24*60)
        
    colors = [get_co2_color(val) for val in plot_data['CO2(ppm)']]
    
    ax_strip.bar(plot_data['Date'], height=1, width=width*1.2, color=colors, align='edge', rasterized=True)
    ax_strip.set_ylim(0, 1)
    ax_strip.set_yticks([])
    ax_strip.set_xlim(x_min, x_max)
    
    plt.setp(ax_strip.get_xticklabels(), visible=False)
    ax_strip.tick_params(axis='x', which='both', length=0)
    ax_strip.grid(False) # Clean color strip, no lines
    # --- Draw Ruler (Right) ---
    ax_ruler.set_yticks([])
    ax_ruler.set_ylim(0, 1)
    
    # Re-enable spines to create the "Cadre" (Frame)
    for spine in ax_ruler.spines.values():
        spine.set_visible(True)
        spine.set_color('#888888') # Grey frame
        
    ax_ruler.grid(True, which='major', axis='x', color='#888888', linestyle='-', linewidth=1)
    # Disable minor grid so we only see the "small lines" from ticks
    ax_ruler.grid(False, which='minor', axis='x')
    # --- Shading on Ruler (Match Graph) ---
    # We repeat the shading logic for the ruler to match the photo
    current_day_r = x_min.replace(hour=0, minute=0, second=0, microsecond=0)
    end_plot_day_r = x_max.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    
    while current_day_r < end_plot_day_r:
        weekday = current_day_r.weekday()
        if weekday in schedule:
            open_h, open_m, close_h, close_m = schedule[weekday]
            opening_time = current_day_r + datetime.timedelta(hours=open_h, minutes=open_m)
            closing_time = current_day_r + datetime.timedelta(hours=close_h, minutes=close_m)
            ax_ruler.axvspan(opening_time, closing_time, facecolor='#eef5f9', alpha=1.0, zorder=0) 
        current_day_r += datetime.timedelta(days=1)
    
    # --- Ticks Strategy: Major = Days, Minor = Hours (08, 16) ---
    # Major: Midnight (Days)
    ax_ruler.xaxis.set_major_locator(mdates.DayLocator())
    ax_ruler.xaxis.set_major_formatter(mdates.DateFormatter('%a %d'))
    
    # Minor: Hours 08:00 and 16:00 (Restored as per photo)
    ax_ruler.xaxis.set_minor_locator(mdates.HourLocator(byhour=[8, 16]))
    ax_ruler.xaxis.set_minor_formatter(mdates.DateFormatter('%H:00'))
    
    # Tick Parameters (Lengths)
    # Major (Days): Look like full grid lines (handled by grid mainly, but tick adds to it)
    # Minor (Hours): Short lines (length=25) inside. NO GRID for these.
    ax_ruler.tick_params(axis='x', which='major', direction='in', length=0, width=0, pad=10, labelsize=9, zorder=5, labeltop=False, labelbottom=True)
    # Minor: Lighter color for the "small lines"
    ax_ruler.tick_params(axis='x', which='minor', direction='in', length=25, width=1, color='#BBBBBB', pad=10, labelsize=9, zorder=5, labeltop=False, labelbottom=True)
    
    # Rotate Labels
    plt.setp(ax_ruler.get_xticklabels(which='both'), rotation=-90, ha='center', va='top')
    
    # Bold Major Labels (Days)
    plt.setp(ax_ruler.get_xticklabels(which='major'), fontweight='bold')
    
    # Hide Strip Labels explicitly (Major AND Minor)
    plt.setp(ax_strip.get_xticklabels(which='both'), visible=False)
    ax_strip.tick_params(axis='x', which='both', labelbottom=False, labeltop=False, bottom=False, top=False)
    
    # Ensure Graph labels are also dead
    plt.setp(ax_graph.get_xticklabels(which='both'), visible=False)
    ax_graph.tick_params(axis='x', which='both', labelbottom=False, labeltop=False, bottom=False, top=False)
    
    ax_ruler.set_xlim(x_min, x_max)
    print(f"Saving graph to {OUTPUT_PATH}")
    plt.savefig(OUTPUT_PATH, dpi=100, bbox_inches='tight')
    plt.close()
if __name__ == "__main__":
    df = load_data(CSV_PATH)
    if df is not None:
        plot_co2_graph(df)
