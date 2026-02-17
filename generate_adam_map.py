import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Adam_Season_Tactical_Map.png'

# Adam's Player IDs (Verified from API GW26)
ADAM_IDS = [1, 531, 225, 694, 450, 238, 16, 417, 97, 430, 310, 470, 615, 317, 725]

# Tactical Coordinates (x: 0-100, y: 0-100)
COORDINATES = {
    'Raya': (50, 10),
    'Dúbravka': (50, 5),
    'James': (85, 48),
    'Mukiele': (75, 40),
    'Ballard': (45, 32),
    'Hincapie': (20, 50),
    'Andersen': (35, 35),
    'Saka': (82, 75),
    'Estêvão': (18, 72),
    'Cunha': (55, 65),
    'Cherki': (40, 68),
    'Summerville': (30, 75),
    'Haaland': (52, 88),
    'Evanilson': (40, 82),
    'Barry': (65, 82)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    team_stats = []
    print(f"{'ID':<5} | {'Name':<15} | {'xG':<5} | {'xA':<5}")
    print("-" * 40)
    
    for pid in ADAM_IDS:
        p = next((x for x in players_static if x['id'] == pid), None)
        if p:
            name = p['web_name']
            xg = float(p['expected_goals'])
            xa = float(p['expected_assists'])
            xgc = float(p['expected_goals_conceded'])
            
            print(f"{pid:<5} | {name:<15} | {xg:<5.1f} | {xa:<5.1f}")
            
            team_stats.append({
                'name': name,
                'pts': p['total_points'],
                'xG': xg,
                'xA': xa,
                'xGC': xgc,
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#eef7ee') # Light readable pitch
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        
        # Color Coding: GK=1, DEF=2, MID=3, FWD=4
        colors = {1: '#FFD700', 2: '#1E90FF', 3: '#FF4500', 4: '#32CD32'}
        color = colors.get(p['pos_id'], 'white')
        
        # Draw Player Node
        ax.scatter(x, y, s=1600, color=color, edgecolors='black', linewidth=1.5, zorder=5)
        
        # Player Label
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=8, fontweight='bold', zorder=6, color='black')
        
        # Stats Label
        stats_str = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_str, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#222222', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("ADAM: SEASON TACTICAL MAP\nCurrent Squad Performance (GW26)", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Adam Map Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
