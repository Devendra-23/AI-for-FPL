import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Tommy_Season_Tactical_Map.png'

# Tommy's Player IDs (Verified from API GW26)
TOMMY_IDS = [1, 8, 5, 224, 373, 517, 488, 82, 237, 430, 661, 670, 136, 531, 660]

# Tactical Coordinates (x: 0-100, y: 0-100)
COORDINATES = {
    'Raya': (50, 10),
    'Roefs': (50, 5),
    'Gabriel': (35, 30),
    'J.Timber': (85, 48),
    'Virgil': (50, 32),
    'Cucurella': (20, 45),
    'Ballard': (65, 35),
    'Semenyo': (82, 72),
    'Enzo': (45, 60),
    'Bruno G.': (55, 58),
    'Anderson': (30, 68),
    'Stach': (65, 65),
    'Haaland': (52, 88),
    'Ekitiké': (40, 82),
    'Thiago': (65, 80)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    team_stats = []
    print(f"{'ID':<5} | {'Name':<15} | {'xG':<5} | {'xA':<5}")
    print("-" * 40)
    
    for pid in TOMMY_IDS:
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

    plt.title("TOMMY: SEASON TACTICAL MAP\nCurrent Squad Performance (GW26)", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Tommy Map Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
