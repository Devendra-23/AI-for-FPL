import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Forest_Pereira_Tactical_Map.png'

# Projected Forest 3-4-2-1 under Vítor Pereira
FOREST_SQUAD = [
    {'name': 'Sels', 'pos': (50, 10), 'color': '#FFD700', 'role': 'GK'},
    {'name': 'Murillo', 'pos': (30, 25), 'color': '#1E90FF', 'role': 'LCB (Ball Progressor)'},
    {'name': 'Milenkovic', 'pos': (50, 25), 'color': '#1E90FF', 'role': 'CCB'},
    {'name': 'Boly', 'pos': (70, 25), 'color': '#1E90FF', 'role': 'RCB'},
    {'name': 'Aina', 'pos': (15, 55), 'color': '#1E90FF', 'role': 'LWB (High)'},
    {'name': 'N.Williams', 'pos': (85, 55), 'color': '#1E90FF', 'role': 'RWB (Overlap)'},
    {'name': 'Sangaré', 'pos': (40, 45), 'color': '#FF4500', 'role': 'CM (Holder)'},
    {'name': 'Anderson', 'pos': (60, 45), 'color': '#FF4500', 'role': 'CM (Box-to-Box)'},
    {'name': 'Hudson-Odoi', 'pos': (30, 75), 'color': '#FF4500', 'role': 'Dual 10 (Left)'},
    {'name': 'Gibbs-White', 'pos': (70, 75), 'color': '#FF4500', 'role': 'Dual 10 (Talisman)'},
    {'name': 'Awoniyi', 'pos': (50, 88), 'color': '#32CD32', 'role': 'ST (Target Man)'}
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

    for p in FOREST_SQUAD:
        x, y = p['pos']
        ax.scatter(x, y, s=1800, color=p['color'], edgecolors='black', linewidth=1.5, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')
        
        # Role Label
        ax.text(x, y-7, p['role'], ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#222222', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("NOTTINGHAM FOREST: THE VITOR PEREIRA SYSTEM\nExpected 3-4-2-1 Setup (New Manager Bounce)", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
