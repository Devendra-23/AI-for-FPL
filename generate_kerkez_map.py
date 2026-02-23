import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Dev_Tactical_Kerkez_Explosion.png'

# Dev's Squad with Kerkez (Aggressive Setup)
KERKEZ_SQUAD = [
    {'name': 'Raya', 'pos': (50, 10), 'color': '#FFD700', 'stats': 'xGC: 1.5'},
    {'name': 'Gabriel', 'pos': (35, 30), 'color': '#1E90FF', 'stats': 'xG: 0.12'},
    {'name': 'Kerkez', 'pos': (18, 55), 'color': '#e32221', 'stats': 'xA: 0.32 (Elite)'}, # High and wide for Liverpool
    {'name': 'Muñoz', 'pos': (85, 45), 'color': '#1E90FF', 'stats': 'xA: 0.89'},
    {'name': 'Mbeumo', 'pos': (75, 75), 'color': '#FF4500', 'stats': 'xGI: 0.22'},
    {'name': 'Semenyo', 'pos': (82, 60), 'color': '#FF4500', 'stats': 'GW26: 14pts'},
    {'name': 'Haaland', 'pos': (52, 88), 'color': '#32CD32', 'stats': 'xG: 20.2'}
]

def main():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_facecolor('#eef7ee')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in KERKEZ_SQUAD:
        x, y = p['pos']
        # Red highlight for Kerkez
        edge = 'red' if p['name'] == 'Kerkez' else 'black'
        lw = 3 if p['name'] == 'Kerkez' else 1.5
        
        ax.scatter(x, y, s=1800, color=p['color'], edgecolors=edge, linewidth=lw, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Stats Label
        ax.text(x, y-7, p['stats'], ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("DEV: THE KERKEZ EXPLOSION MAP\nAggressive Left-Back Positioning for GW27+", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
