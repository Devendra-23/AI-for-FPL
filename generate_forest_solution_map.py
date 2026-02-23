import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Forest_Blank_Solution_Map.png'

# FOREST SOLUTION SQUAD (Targeting BGW31 Coverage)
FOREST_TARGETS = [
    {'name': 'Ortega', 'pos': (50, 10), 'color': '#FFD700', 'note': 'GK Option for Raya (GW31)'},
    {'name': 'Murillo', 'pos': (28, 30), 'color': '#1E90FF', 'note': 'Target for Muñoz (GW28)'},
    {'name': 'N.Williams', 'pos': (88, 65), 'color': '#1E90FF', 'note': 'Cheap BGW31 Bench'},
    {'name': 'Gibbs-White', 'pos': (68, 80), 'color': '#FF4500', 'note': 'Target for Rogers (GW29)'},
    {'name': 'Hudson-Odoi', 'pos': (32, 78), 'color': '#FF4500', 'note': 'Differential for BGW31'},
    {'name': 'Igor Thiago', 'pos': (52, 90), 'color': '#32CD32', 'note': 'UEL Goalscorer (FIT)'}
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

    for p in FOREST_TARGETS:
        x, y = p['pos']
        ax.scatter(x, y, s=2000, color=p['color'], edgecolors='black', linewidth=2, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Action Label
        ax.text(x, y-7, p['note'], ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#222222', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("FOREST: THE BGW31 SOLUTION\nKey Targets to Replace Blanking City/Palace/Arsenal Assets", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
