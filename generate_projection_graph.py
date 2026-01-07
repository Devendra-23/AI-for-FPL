
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- 1. Define Baseline Data (Estimated from recent form/xGI) ---
# Average Points Per Gameweek (Conservative Estimates)
current_squad_avg = 52  # Based on recent GW19/20 performance (approx)
new_squad_avg = 62      # Uplift from Palmer, Watkins, Mbeumo, Hall

# --- 2. Simulation Timeline (GW21 to GW26) ---
gameweeks = np.array([20, 21, 22, 23, 24, 25, 26])
current_total_score = 1050 # Estimated current season total (Baseline)

# --- 3. Scenario 1: Do Nothing (Maintain Current Squad) ---
# Accumulate ~52 points per week
points_no_changes = [current_total_score]
for _ in range(6):
    points_no_changes.append(points_no_changes[-1] + current_squad_avg)

# --- 4. Scenario 2: The "Power Shift" Strategy ---
# GW21-22: Roll (Same output as current)
# GW23: Mini-Wildcard (Output jumps)
# GW24-26: Higher average
points_strategy = [current_total_score]

# GW21 (Roll)
points_strategy.append(points_strategy[-1] + current_squad_avg) 
# GW22 (Roll)
points_strategy.append(points_strategy[-1] + current_squad_avg)
# GW23 (4 Transfers: Palmer, Watkins, Mbeumo, Hall) - Immediate Impact
points_strategy.append(points_strategy[-1] + new_squad_avg)
# GW24 (Watkins fully integrated)
points_strategy.append(points_strategy[-1] + new_squad_avg)
# GW25 (Robinson/Timber swap - Defensive solidity)
points_strategy.append(points_strategy[-1] + new_squad_avg + 2) # Slight boost for Robinson CBIT
# GW26
points_strategy.append(points_strategy[-1] + new_squad_avg + 2)

# --- 5. Plotting ---
plt.figure(figsize=(12, 6))

# Plot Lines
plt.plot(gameweeks, points_no_changes, label='Current Squad Trajectory', color='grey', linestyle='--', marker='o')
plt.plot(gameweeks, points_strategy, label='Power Shift Strategy (GW23)', color='#00ff85', linewidth=3, marker='D') # FPL Green

# Annotations
plt.axvline(x=23, color='red', linestyle=':', alpha=0.5)
plt.text(23.1, points_strategy[3], 'GW23: 4-Transfer Overhaul\n(Palmer, Watkins, Mbeumo)', color='red', fontweight='bold')

plt.axvline(x=25, color='blue', linestyle=':', alpha=0.5)
plt.text(25.1, points_strategy[5], 'GW25: Robinson (CBIT)', color='blue', fontweight='bold')

# Styling
plt.title('Projected Points: "Diamond Hands" Strategy vs. Status Quo', fontsize=14, fontweight='bold')
plt.xlabel('Gameweek', fontsize=12)
plt.ylabel('Total Points', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Save
output_path = 'Dev_Projected_Performance.png'
plt.savefig(output_path, dpi=300)
print(f"Graph saved to: {output_path}")
