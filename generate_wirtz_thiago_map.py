import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Wirtz_vs_Thiago_Tactical.png'

# Tactical Positioning Data
DATA = [
    {'name': 'Wirtz', 'pos': (65, 75), 'color': '#e32221', 'stats': 'xG: 5.6 | xA: 4.1'}, # Liverpool Inverted 10
    {'name': 'Thiago', 'pos': (50, 90), 'color': '#e30613', 'stats': 'xG: 14.7 | xA: 1.1'} # Brentford Box Predator
]

def main():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_facecolor('#eef7ee')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in DATA:
        x, y = p['pos']
        ax.scatter(x, y, s=2500, color=p['color'], edgecolors='black', linewidth=2, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=12, fontweight='bold', zorder=6, color='white')
        
        # Stats Label
        ax.text(x, y-8, p['stats'], ha='center', va='top', fontsize=10, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("GW27 SCOUT: WIRTZ (LIV) VS. THIAGO (BRE)\nPositional Dominance & Seasonal Metrics", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(50, 100) # Focusing on attacking half
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
