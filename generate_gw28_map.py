import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Dev_GW28_Pivot_Master.png'

# Dev's NEW Squad (Post-GW28 Transfers)
PIVOT_SQUAD = [
    {'name': 'Raya', 'pos': (50, 10), 'color': '#FFD700', 'stats': 'xGC: 1.5'},
    {'name': 'Gabriel', 'pos': (35, 30), 'color': '#1E90FF', 'stats': 'Set-Piece Threat'},
    {'name': 'Virgil', 'pos': (50, 32), 'color': '#e32221', 'stats': 'CBIT Dominator (LIV)'},
    {'name': 'Hill', 'pos': (15, 35), 'color': '#af122a', 'stats': 'Budget Enabler (BOU)'},
    {'name': 'Mbeumo', 'pos': (75, 75), 'color': '#FF4500', 'stats': 'xGI: 0.22'},
    {'name': 'B.Fernandes', 'pos': (55, 65), 'color': '#FF4500', 'stats': 'Main Playmaker'},
    {'name': 'Thiago', 'pos': (50, 90), 'color': '#e30613', 'stats': '14.7 xG (BRE)'},
    {'name': 'Haaland', 'pos': (52, 88), 'color': '#32CD32', 'stats': 'xG: 20.2'},
    {'name': 'Semenyo', 'pos': (82, 60), 'color': '#FF4500', 'stats': 'GW26 Haul (14pts)'}
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

    for p in PIVOT_SQUAD:
        x, y = p['pos']
        # Highlight New Players
        edge = 'gold' if p['name'] in ['Virgil', 'Thiago', 'Hill'] else 'black'
        lw = 3 if p['name'] in ['Virgil', 'Thiago', 'Hill'] else 1.5
        
        ax.scatter(x, y, s=1800, color=p['color'], edgecolors=edge, linewidth=lw, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Stats Label
        ax.text(x, y-7, p['stats'], ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("DEV: GW28 PIVOT MASTERPLAN\nNew Assets Integrated: Virgil, Igor Thiago, Hill", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
