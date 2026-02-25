import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Dev_Actual_AvgPos_Map_GW28.png'

# Dev's NEW Squad (Verified Post-GW27 Transfers)
SQUAD_NAMES = [
    'Raya', 'Gabriel', 'Virgil', 'Hill', 'Alderete', 
    'Mbeumo', 'B.Fernandes', 'Semenyo', 'Enzo', 'Rogers', 
    'Haaland', 'Thiago', 'Dúbravka', 'Calvert-Lewin', 'Gudmundsson'
]

# Tactical Coordinates (Standardized from v2 map)
COORDINATES = {
    'Raya': (50, 10),
    'Dúbravka': (50, 5),
    'Gabriel': (35, 30),
    'Virgil': (50, 32),
    'Hill': (15, 35),
    'Alderete': (80, 35),
    'Mbeumo': (75, 75),
    'B.Fernandes': (55, 68),
    'Semenyo': (82, 60),
    'Enzo': (45, 55),
    'Rogers': (30, 65),
    'Haaland': (52, 88),
    'Thiago': (45, 82),
    'Calvert-Lewin': (40, 85),
    'Gudmundsson': (20, 55)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    team_stats = []
    for name in SQUAD_NAMES:
        # Match by web_name or part of name
        p = next((x for x in players_static if x['web_name'] == name or (name in x['web_name'] and x['team'] != 0)), None)
        if p:
            team_stats.append({
                'name': p['web_name'],
                'pts': p['total_points'],
                'xG': float(p['expected_goals']),
                'xA': float(p['expected_assists']),
                'xGC': float(p['expected_goals_conceded']),
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(14, 16))
    ax.set_facecolor('#eef7ee') # High readability pitch
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        # GK=1, DEF=2, MID=3, FWD=4
        colors = {1: '#FFD700', 2: '#1E90FF', 3: '#FF4500', 4: '#32CD32'}
        color = colors.get(p['pos_id'], 'white')
        
        # Highlight new core
        edge = 'gold' if p['name'] in ['Virgil', 'Thiago', 'Hill'] else 'black'
        lw = 3 if p['name'] in ['Virgil', 'Thiago', 'Hill'] else 1.5
        
        ax.scatter(x, y, s=1800, color=color, edgecolors=edge, linewidth=lw, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Stats Label
        stats_str = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_str, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("DEV: LATEST AVERAGE POSITIONAL MAP (GW28)\nIntegrated Virgil, Igor Thiago, & Hill | Full Season Metrics", 
              color='black', fontsize=20, fontweight='bold', pad=40)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Updated Map Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
