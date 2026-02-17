import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Chris_Season_Overall_Tactical_Map.png'

# Tactical Coordinates (Standardized for Chris's Season Roles)
COORDINATES = {
    'Dúbravka': (50, 12),
    'Gabriel': (35, 35),
    'J.Timber': (85, 55),
    'Hall': (25, 62), # High attacking LB for Newcastle
    'Mukiele': (75, 45),
    'Lucas Pires': (15, 55),
    'Palmer': (70, 75), # Drifting right
    'Rice': (45, 50), # Deeper mid
    'Rogers': (30, 68),
    'Wilson': (80, 70), # Wide right for Fulham
    'Mbeumo': (75, 78),
    'Cunha': (55, 75), # Shadow striker role
    'Haaland': (50, 88),
    'Igor Jesus': (60, 82),
    'Kroupi.Jr': (65, 80),
    'Darlow': (50, 10)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    # Chris's Squad
    team_names = [
        "Dúbravka", "Gabriel", "J.Timber", "Hall", "Mukiele", 
        "Lucas Pires", "Palmer", "Rice", "Rogers", "Wilson", 
        "Mbeumo", "Cunha", "Haaland", "Igor Jesus", "Kroupi.Jr", "Darlow"
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
    ax.set_facecolor('#4b0082') # Indigo/Dark Purple for Chris's "Sniper" strategy
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1, alpha=0.5)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1, alpha=0.5)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        colors = {1: '#f8d210', 2: '#ffffff', 3: '#ff4d4d', 4: '#00cc00'}
        color = colors.get(p['pos_id'], 'white')
        
        ax.scatter(x, y, s=1200, color=color, edgecolors='black', zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        stats_text = f"Pts: {p['pts']}\nxG: {p['xG']:.1f}\nxA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_text, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.title("CHRIS'S SEASON OVERALL\nAvg Positions & Tactical Stats 2025/26", 
              color='white', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#4b0082')
    print(f"Chris Season Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
