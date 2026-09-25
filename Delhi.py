import csv
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# 1. READ DATA 

data = []

with open('POWER_Point_Daily_19840101_20260101_028d61N_077d21E_UTC.csv', 'r') as f:
    for line in f:
        if line.startswith('YEAR'):
            break
    reader = csv.DictReader(f, fieldnames=['YEAR', 'DOY', 'T2M', 'T2M_MAX', 'T2M_MIN'])
    for row in reader:
        try:
            year    = int(row['YEAR'])
            t2m     = float(row['T2M'])
            t2m_max = float(row['T2M_MAX'])
            t2m_min = float(row['T2M_MIN'])
            if t2m != -999 and 1984 <= year <= 2023:
                data.append((year, t2m, t2m_max, t2m_min))
        except:
            pass

# 2. GROUP BY YEAR 

yearly_t2m   = defaultdict(list)
yearly_range = defaultdict(list)

for year, t2m, t2m_max, t2m_min in data:
    yearly_t2m[year].append(t2m)
    yearly_range[year].append(t2m_max - t2m_min)

# 3. CALCULATE STATS PER YEAR 

years      = []
mean_temp  = []
std_temp   = []
mean_range = []

for year in sorted(yearly_t2m.keys()):
    vals  = yearly_t2m[year]
    n     = len(vals)
    mean  = sum(vals) / n
    std   = math.sqrt(sum((x - mean) ** 2 for x in vals) / n)
    rang  = sum(yearly_range[year]) / len(yearly_range[year])

    years.append(year)
    mean_temp.append(mean)
    std_temp.append(std)
    mean_range.append(rang)

    print(f"{year}  |  Mean: {mean:.2f}°C  |  Std Dev: {std:.2f}°C  |  Daily Range: {rang:.2f}°C")

# 4. PLOT 

fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.suptitle('Delhi Temperature Analysis (1984–2023)\nNASA POWER MERRA-2 Data',
             fontsize=14, fontweight='bold')

datasets = [
    (mean_temp,  'tomato',    'darkred',   'Annual Mean Temperature',              'Temperature (°C)'),
    (std_temp,   'steelblue', 'navy',      'Annual Temperature Variability (Std Dev)', 'Std Dev (°C)'),
    (mean_range, 'seagreen',  'darkgreen', 'Mean Daily Temperature Range (Max−Min)', 'Range (°C)'),
]

for ax, (vals, col, tcol, title, ylabel) in zip(axes, datasets):
    z = np.polyfit(years, vals, 1)
    p = np.poly1d(z)
    ax.plot(years, vals, 'o-', color=col, linewidth=1.5, markersize=4)
    ax.plot(years, p(years), '--', color=tcol, linewidth=1.5,
            label=f'Trend: {z[0]:+.4f}°C/yr')
    ax.set_title(title, fontsize=12)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1983, 2024)

axes[2].set_xlabel('Year')

plt.tight_layout()
plt.savefig('delhi_temperature_analysis.png', dpi=150, bbox_inches='tight')
print("\nPlot saved as delhi_temperature_analysis.png")
