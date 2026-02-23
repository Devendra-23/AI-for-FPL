import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Forest_Actual_AvgPos_Map_UEL.png'

# ACTUAL AVG POSITIONS (Based on UEL vs Fenerbahçe)
FOREST_ACTUAL = [
    {'name': 'Sels', 'pos': (50, 8), 'color': '#FFD700', 'stats': 'xGC: 0.6 | CS: 1'},
    {'name': 'Murillo', 'pos': (28, 30), 'color': '#1E90FF', 'stats': 'xGI: 0.13 | CBIT: 8'},
    {'name': 'Milenkovic', 'pos': (50, 25), 'color': '#1E90FF', 'stats': 'xGC: 0.6'},
    {'name': 'Boly', 'pos': (72, 28), 'color': '#1E90FF', 'stats': 'xGC: 0.6'},
    {'name': 'Aina', 'pos': (12, 62), 'color': '#1E90FF', 'stats': 'xA: 0.15 | xG: 0.02'},
    {'name': 'N.Williams', 'pos': (88, 65), 'color': '#1E90FF', 'stats': 'xA: 0.45 | Assist: 1'},
    {'name': 'Sangaré', 'pos': (42, 48), 'color': '#FF4500', 'stats': 'Tackles: 4 | xGC: 0.6'},
    {'name': 'Anderson', 'pos': (58, 52), 'color': '#FF4500', 'stats': 'xA: 0.15 | Assist: 1'},
    {'name': 'Hudson-Odoi', 'pos': (32, 78), 'color': '#FF4500', 'stats': 'xG: 0.48 | Goal: 1'},
    {'name': 'Gibbs-White', 'pos': (68, 80), 'color': '#FF4500', 'stats': 'xGI: 1.03 | G: 1, A: 1'},
    {'name': 'Igor Thiago', 'pos': (52, 90), 'color': '#32CD32', 'stats': 'xG: 1.15 | Goal: 1'}
]

def main():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#eef7ee') # Light readable pitch
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in FOREST_ACTUAL:
        x, y = p['pos']
        ax.scatter(x, y, s=1800, color=p['color'], edgecolors='black', linewidth=1.5, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Stats Label
        ax.text(x, y-7, p['stats'], ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("NOTTINGHAM FOREST: ACTUAL UEL AVG POSITIONS\nFenerbahçe 0-3 Forest (Feb 10, 2026)", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
