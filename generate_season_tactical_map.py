import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Dev_Season_Overall_Tactical_Map.png'

# Tactical Coordinates (Standardized for Season Roles)
COORDINATES = {
    'Raya': (50, 12),
    'Gabriel': (38, 35),
    'J.Timber': (82, 55),
    'Muñoz': (85, 60),
    'Alderete': (25, 35),
    'Van Hecke': (50, 32),
    'Mbeumo': (75, 75),
    'B.Fernandes': (50, 65),
    'Rogers': (35, 68),
    'Semenyo': (80, 72),
    'Enzo': (45, 52),
    'Haaland': (55, 85),
    'Calvert-Lewin': (45, 82),
    'Kroupi.Jr': (65, 80),
    'Gudmundsson': (20, 50)
}

def main():
    # 1. Load Data
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    # Current Team List (15 players)
    team_names = [
        "Raya", "Gabriel", "J.Timber", "Muñoz", "Alderete", 
        "Van Hecke", "Mbeumo", "B.Fernandes", "Rogers", "Semenyo", 
        "Enzo", "Haaland", "Calvert-Lewin", "Kroupi.Jr", "Gudmundsson"
    ]
    
    # 2. Extract Season Stats
    team_stats = []
    for name in team_names:
        p = next((x for x in players_static if name in x['web_name'] or x['web_name'] in name), None)
        if p:
            team_stats.append({
                'name': p['web_name'],
                'pts': p['total_points'],
                'xG': float(p['expected_goals']),
                'xA': float(p['expected_assists']),
                'xGC': float(p['expected_goals_conceded']),
                'xGI': float(p['expected_goal_involvements']),
                'pos_id': p['element_type']
            })

    # 3. Draw Pitch
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#1e5d2b')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1, alpha=0.5)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1, alpha=0.5)
    ax.add_artist(center_circle)

    # 4. Plot Players
    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        
        # Color based on position (GK, DEF, MID, FWD)
        colors = {1: '#f8d210', 2: '#005fcc', 3: '#ff4d4d', 4: '#ffffff'}
        color = colors.get(p['pos_id'], 'white')
        
        ax.scatter(x, y, s=1200, color=color, edgecolors='black', zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6)
        
        # Stats Box
        stats_text = f"Pts: {p['pts']}\nxG: {p['xG']:.1f}\nxA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_text, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='black', alpha=0.6, boxstyle='round,pad=0.3'))

    plt.title("SEASON OVERALL: AVG POSITIONS & TACTICAL STATS\n(Dev's Squad Performance 2025/26)", 
              color='white', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#1e5d2b')
    print(f"Season Overall Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
