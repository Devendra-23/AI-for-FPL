import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Chris_Current_Season_Tactical_Map.png'

# Tactical Coordinates for Chris's CURRENT Squad
COORDINATES = {
    'Dúbravka': (50, 10),
    'Darlow': (50, 8),
    'Gabriel': (35, 32),
    'J.Timber': (85, 52),
    'Hall': (22, 60),      # Lewis Hall (High attacking LB)
    'Mukiele': (78, 42),
    'Lucas Pires': (18, 52),
    'Palmer': (72, 75),
    'Rice': (45, 48),
    'Rogers': (32, 65),
    'Wilson': (82, 70),
    'Mbeumo': (75, 78),
    'Cunha': (55, 72),
    'Haaland': (52, 88),
    'Igor Jesus': (58, 80),
    'Kroupi.Jr': (65, 82)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    # Current Team from fetch results
    team_names = [
        "Dúbravka", "Hall", "J.Timber", "Gabriel", "Palmer", 
        "Rogers", "Wilson", "Cunha", "Rice", "Haaland", 
        "Kroupi.Jr", "Darlow", "Igor Jesus", "Mukiele", "Lucas Pires"
    ]
    
    team_stats = []
    for name in team_names:
        # Match by web_name exactly or containing
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

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#2b2b2b') # Sleek dark background
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        # GK=1, DEF=2, MID=3, FWD=4
        colors = {1: '#f1c40f', 2: '#3498db', 3: '#e74c3c', 4: '#2ecc71'}
        color = colors.get(p['pos_id'], 'white')
        
        ax.scatter(x, y, s=1300, color=color, edgecolors='white', linewidth=2, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        stats_text = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_text, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.8, boxstyle='round,pad=0.3'))

    plt.title("CHRIS: SEASON PERFORMANCE MAP\nLewis Hall & Current Squad (2025/26)", 
              color='white', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#2b2b2b')
    print(f"Chris Updated Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
