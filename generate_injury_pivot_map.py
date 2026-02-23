import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Treatment_Room_Pivot_GW27.png'

# The Shift in Value (Wirtz/Isak OUT -> Thiago/Bowen IN)
DATA = [
    {'name': 'Wirtz', 'pos': (65, 75), 'color': 'gray', 'stats': 'OUT (2-3 Weeks)'},
    {'name': 'Isak', 'pos': (50, 88), 'color': 'gray', 'stats': 'OUT (Till April)'},
    {'name': 'Thiago', 'pos': (50, 90), 'color': '#e30613', 'stats': 'TARGET (14.7 xG)'},
    {'name': 'Bowen', 'pos': (85, 70), 'color': '#7A263A', 'stats': 'TARGET (GW31 Insurance)'}
]

def main():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_facecolor('#f0f0f0') # Grayish pitch to reflect injury crisis
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)

    for p in DATA:
        x, y = p['pos']
        ax.scatter(x, y, s=2500, color=p['color'], edgecolors='black', linewidth=2, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=12, fontweight='bold', zorder=6, color='white')
        
        # Stats Label
        ax.text(x, y-8, p['stats'], ha='center', va='top', fontsize=10, color='black', 
                fontweight='bold', bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("GW27 TREATMENT ROOM PIVOT\nAbandoning Injured Premiums for Fit Differentials", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(50, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#f0f0f0')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
