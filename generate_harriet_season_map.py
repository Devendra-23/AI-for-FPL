import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Harriet_Season_Overall_Tactical_Map.png'

# Tactical Coordinates (Standardized for Season Roles)
COORDINATES = {
    'Raya': (50, 12),
    'Gabriel': (38, 35),
    'Muñoz': (85, 60),
    'Senesi': (50, 38),
    'Van Hecke': (45, 32),
    'Mukiele': (25, 45),
    'Mbeumo': (75, 75),
    'B.Fernandes': (50, 65),
    'Rice': (45, 55),
    'Enzo': (42, 58),
    'Rogers': (35, 68),
    'Haaland': (55, 85),
    'Calvert-Lewin': (45, 82),
    'Kroupi.Jr': (65, 80),
    'Dúbravka': (50, 12)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    # Harriet's Squad
    team_names = [
        "Raya", "Gabriel", "Muñoz", "Senesi", "Van Hecke", 
        "Mukiele", "Mbeumo", "B.Fernandes", "Rice", "Enzo", 
        "Rogers", "Haaland", "Calvert-Lewin", "Kroupi.Jr", "Dúbravka"
    ]
    
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
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#4169E1') # Royal Blue for Harriet's "Title Charge"
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1, alpha=0.5)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1, alpha=0.5)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        colors = {1: '#f8d210', 2: '#ffffff', 3: '#ff4d4d', 4: '#000000'}
        color = colors.get(p['pos_id'], 'white')
        
        ax.scatter(x, y, s=1200, color=color, edgecolors='black', zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black' if color=='#ffffff' else 'white')
        
        stats_text = f"Pts: {p['pts']}\nxG: {p['xG']:.1f}\nxA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_text, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.title("HARRIET'S SEASON OVERALL\nAvg Positions & Tactical Stats 2025/26", 
              color='white', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#4169E1')
    print(f"Harriet Season Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
