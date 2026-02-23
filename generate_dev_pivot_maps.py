import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration
JSON_FILE = 'fpl_data.json'

# Common Coordinates for Dev's Squad
BASE_COORDS = {
    'Raya': (50, 10),
    'Gabriel': (35, 30),
    'Timber': (65, 30),
    'Virgil': (50, 35), # Centrally dominant
    'Muñoz': (85, 45),
    'Alderete': (15, 35),
    'Mbeumo': (75, 75),
    'B.Fernandes': (55, 68),
    'Rogers': (30, 65),
    'Semenyo': (82, 60),
    'Enzo': (45, 55),
    'Haaland': (52, 88),
    'Calvert-Lewin': (40, 82)
}

def generate_map(player_list, title, filename):
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    team_stats = []
    for name in player_list:
        p = next((x for x in players_static if x['web_name'] == name), None)
        if p:
            team_stats.append({
                'name': name,
                'pts': p['total_points'],
                'xG': float(p['expected_goals']),
                'xA': float(p['expected_assists']),
                'xGC': float(p['expected_goals_conceded']),
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#eef7ee')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = BASE_COORDS.get(p['name'], (50, 50))
        colors = {1: '#FFD700', 2: '#1E90FF', 3: '#FF4500', 4: '#32CD32'}
        color = colors.get(p['pos_id'], 'white')
        
        # Highlight Virgil
        edge = 'red' if p['name'] == 'Virgil' else 'black'
        lw = 3 if p['name'] == 'Virgil' else 1.5
        
        ax.scatter(x, y, s=1600, color=color, edgecolors=edge, linewidth=lw, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6)
        
        # Stats Label
        stats_str = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_str, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#222222', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title(title, color='black', fontsize=18, fontweight='bold', pad=30)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    plt.savefig(filename, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {filename}")

# Scenario 1: Without Virgil (Current Arsenal Trap)
generate_map(
    ['Raya', 'Gabriel', 'Timber', 'Muñoz', 'Alderete', 'Mbeumo', 'B.Fernandes', 'Rogers', 'Semenyo', 'Enzo', 'Haaland', 'Calvert-Lewin'],
    "DEV: THE ARSENAL TRAP (Current)\nRisk: Concentration & BGW31 Blank",
    "Dev_Tactical_Current_Trap.png"
)

# Scenario 2: With Virgil (The Liverpool Pivot)
generate_map(
    ['Raya', 'Gabriel', 'Virgil', 'Muñoz', 'Alderete', 'Mbeumo', 'B.Fernandes', 'Rogers', 'Semenyo', 'Enzo', 'Haaland', 'Calvert-Lewin'],
    "DEV: THE LIVERPOOL PIVOT (Proposed)\nBenefit: Defensive Diversity & CBIT Points",
    "Dev_Tactical_Virgil_Pivot.png"
)
