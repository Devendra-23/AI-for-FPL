import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Chris_Season_Tactical_Map_Final_v3.png'

# Chris's Player IDs (Verified from API)
CHRIS_IDS = [470, 473, 8, 5, 235, 47, 329, 450, 21, 430, 100, 341, 526, 694, 195]

# Tactical Coordinates (x: 0-100, y: 0-100)
COORDINATES = {
    'Dúbravka': (50, 8),
    'Darlow': (50, 4),
    'Gabriel': (35, 30),
    'J.Timber': (85, 48),
    'Hall': (20, 55),
    'Mukiele': (75, 40),
    'Lucas Pires': (15, 50),
    'Palmer': (70, 72),
    'Rice': (45, 45),
    'Rogers': (30, 62),
    'Wilson': (82, 68),  # Harry Wilson (ID 329)
    'Cunha': (55, 70),
    'Haaland': (50, 88),
    'Igor Jesus': (58, 78),
    'Kroupi.Jr': (65, 80)
}

def main():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    players_static = data['elements']
    
    team_stats = []
    print(f"{'ID':<5} | {'Name':<15} | {'xG':<5} | {'xA':<5}")
    print("-" * 40)
    
    for pid in CHRIS_IDS:
        p = next((x for x in players_static if x['id'] == pid), None)
        if p:
            name = p['web_name']
            xg = float(p['expected_goals'])
            xa = float(p['expected_assists'])
            xgc = float(p['expected_goals_conceded'])
            
            print(f"{pid:<5} | {name:<15} | {xg:<5.1f} | {xa:<5.1f}")
            
            team_stats.append({
                'name': name,
                'display': "Harry Wilson" if name == "Wilson" else name,
                'pts': p['total_points'],
                'xG': xg,
                'xA': xa,
                'xGC': xgc,
                'pos_id': p['element_type']
            })

    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#eef7ee') # Very light pitch green for readability
    
    # Pitch Markings (Darker for light background)
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in team_stats:
        x, y = COORDINATES.get(p['name'], (50, 50))
        
        # Color Coding
        colors = {1: '#FFD700', 2: '#1E90FF', 3: '#FF4500', 4: '#32CD32'}
        color = colors.get(p['pos_id'], 'white')
        
        # Draw Player Node
        ax.scatter(x, y, s=1600, color=color, edgecolors='black', linewidth=1.5, zorder=5)
        
        # Player Label
        ax.text(x, y, p['display'], ha='center', va='center', fontsize=8, fontweight='bold', zorder=6, color='black')
        
        # Stats Label (Black background, white text for contrast on light pitch)
        stats_str = f"xG: {p['xG']:.1f} | xA: {p['xA']:.1f}\nxGC: {p['xGC']:.1f}"
        ax.text(x, y-7, stats_str, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#222222', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("CHRIS: OFFICIAL SEASON TACTICAL MAP\nVerified Harry Wilson (Fulham) & Squad Stats", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig('Chris_Season_Tactical_Map_Final_v4.png', dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Final Map Generated: Chris_Season_Tactical_Map_Final_v4.png")

if __name__ == "__main__":
    main()
