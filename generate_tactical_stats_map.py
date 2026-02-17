import json
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
USER_ID = 17339 
GW = 26
CSV_FILE = 'Dev_Player_Performance.csv'
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Dev_Tactical_Position_Map_GW26.png'

POSITIONS = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}

def get_stats_from_csv(player_name, gw):
    if not os.path.exists(CSV_FILE): return None
    stats = {'xG': 0.0, 'xA': 0.0, 'Pts': 0, 'Min': 0}
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] == player_name:
                try:
                    stats['xG'] = float(row.get(f'GW{gw}_xG', 0.0).replace('-', '0'))
                    stats['xA'] = float(row.get(f'GW{gw}_xA', 0.0).replace('-', '0'))
                    stats['Pts'] = int(row.get(f'GW{gw}_Pts', 0).replace('-', '0'))
                    stats['Min'] = int(row.get(f'GW{gw}_Min', 0).replace('-', '0'))
                except ValueError: pass
                return stats
    return stats

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    elements = data['elements']
    
    # We'll use static coordinates as a base and then "nudge" them
    # GKP: y=10, DEF: y=35, MID: y=60, FWD: y=85
    base_y = {'GKP': 10, 'DEF': 35, 'MID': 60, 'FWD': 85}
    
    # Load GW26 picks (using the latest CSV or local logic)
    # Since I just ran fetch_gw_stats, the CSV is updated.
    # I'll manually define the starters from the fetch output for accuracy
    starters = [
        "Raya", "Muñoz", "Alderete", "Gabriel", "J.Timber",
        "Mbeumo", "B.Fernandes", "Rogers", "Semenyo",
        "Haaland", "Calvert-Lewin"
    ]
    
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_facecolor('#1e5d2b') # Dark Pitch Green
    
    # Draw pitch lines
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 0], [0, 100], 'white', lw=2)
    plt.plot([100, 100], [0, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1)
    ax.add_artist(center_circle)
    
    player_positions = []
    
    # Organize by position to calculate spacing
    pos_groups = {'GKP': [], 'DEF': [], 'MID': [], 'FWD': []}
    for name in starters:
        p_data = next((p for p in elements if p['web_name'] == name or name in p['web_name']), None)
        if p_data:
            pos = POSITIONS[p_data['element_type']]
            pos_groups[pos].append(name)

    for pos, players in pos_groups.items():
        count = len(players)
        if count == 0: continue
        spacing = 100 / (count + 1)
        
        for i, name in enumerate(players):
            stats = get_stats_from_csv(name, GW)
            
            # Base Coordinates
            x = spacing * (i + 1)
            y = base_y[pos]
            
            # TACTICAL NUDGE based on stats
            # High xG/xA moves players forward
            if pos == 'DEF':
                y += (stats['xG'] * 20) + (stats['xA'] * 15)
            elif pos == 'MID':
                y += (stats['xG'] * 10) + (stats['xA'] * 5)
                # Centralize if high xG, widen if high xA
                x += (stats['xA'] - stats['xG']) * 10
            elif pos == 'FWD':
                y += (stats['xG'] * 5)
                x += (stats['xA'] * 10)
            
            # Boundary checks
            x = max(5, min(95, x))
            y = max(5, min(95, y))
            
            # Plot
            color = 'gold' if name == 'Gabriel' else 'white' # TC Gabriel
            ax.scatter(x, y, s=800, color=color, edgecolors='black', zorder=3)
            
            label = f"{name}\n({stats['Pts']}pts)"
            if name == 'Gabriel': label += "\n[TC]"
            
            ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)
            
            # Stats tag
            stats_tag = f"xG: {stats['xG']}\nxA: {stats['xA']}"
            ax.text(x, y-6, stats_tag, ha='center', va='top', fontsize=8, color='yellow', fontweight='bold', bbox=dict(facecolor='black', alpha=0.5, boxstyle='round'))

    plt.title(f"GW{GW} Tactical Performance Map (Dev)\nAvg Pos simulated via xG/xA Aggression", color='white', fontsize=16, pad=20)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#1e5d2b')
    print(f"Tactical Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
