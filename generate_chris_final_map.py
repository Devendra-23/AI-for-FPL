import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Chris_Season_Tactical_Map_Final.png'

# Tactical Coordinates for Chris's EXACT Squad (GW26)
COORDINATES = {
    'Dúbravka': (50, 10),
    'Darlow': (50, 6),
    'Gabriel': (35, 32),
    'J.Timber': (85, 50),
    'Hall': (22, 58),
    'Mukiele': (78, 40),
    'Lucas Pires': (15, 52),
    'Palmer': (70, 75),
    'Rice': (45, 45),
    'Rogers': (30, 65),
    'Wilson': (82, 70), # Harry Wilson (Wide Right)
    'Cunha': (55, 72),
    'Haaland': (50, 88),
    'Igor Jesus': (58, 80),
    'Kroupi.Jr': (65, 82)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    # Absolute Squad from FPL API
    team_names = [
        "Dúbravka", "Hall", "J.Timber", "Gabriel", "Palmer", 
        "Rogers", "Wilson", "Cunha", "Rice", "Haaland", 
        "Kroupi.Jr", "Darlow", "Igor Jesus", "Mukiele", "Lucas Pires"
    ]
    
    team_stats = []
    for name in team_names:
        # Search for Harry Wilson specifically to ensure correct data
        if name == "Wilson":
            p = next((x for x in players_static if x['web_name'] == "Wilson" and x['team'] == 8), None) # Fulham ID is 8
        else:
            p = next((x for x in players_static if x['web_name'] == name), None)
            
        if p:
            team_stats.append({
                'name': p['web_name'],
                'full_name': f"{p['first_name']} {p['second_name']}",
                'pts': p['total_points'],
                'xG': float(p['expected_goals']),
                'xA': float(p['expected_assists']),
                'xGC': float(p['expected_goals_conceded']),
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#1a1a1a')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        colors = {1: '#f1c40f', 2: '#3498db', 3: '#e74c3c', 4: '#2ecc71'}
        color = colors.get(p['pos_id'], 'white')
        
        ax.scatter(x, y, s=1400, color=color, edgecolors='white', linewidth=2, zorder=5)
        
        # Label (Use Harry Wilson for clarity)
        display_name = "Harry Wilson" if p['name'] == "Wilson" else p['name']
        ax.text(x, y, display_name, ha='center', va='center', fontsize=8, fontweight='bold', zorder=6, color='black')
        
        stats_text = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_text, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='black', alpha=0.8, boxstyle='round,pad=0.3'))

    plt.title("CHRIS: COMPLETE SEASON TACTICAL MAP\nFeaturing Harry Wilson & Lewis Hall", 
              color='white', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#1a1a1a')
    print(f"Chris Final Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
