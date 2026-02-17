import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Configuration
OUTPUT_IMAGE = 'Dev_Actual_AvgPos_Map_GW26.png'

# Actual Average Position Coordinates (x: 0-100, y: 0-100)
# Based on GW25/26 Tactical Reports
COORDINATES = {
    'Raya': (50, 15),
    'Gabriel': (35, 38),
    'J.Timber': (85, 62),   # High attacking RB role vs BRE/SUN
    'Muñoz': (88, 58),      # High wingback role
    'Alderete': (25, 35),   # LCB role
    'Mbeumo': (72, 78),     # Drifting inside from right
    'B.Fernandes': (45, 68),# Central playmaker
    'Rogers': (30, 65),     # Left half-space
    'Semenyo': (82, 75),    # High and wide right
    'Haaland': (55, 88),    # Central spearhead
    'Calvert-Lewin': (50, 82), # Traditional #9
    'Enzo': (42, 55),       # Deeper pivot (Bench)
    'Kroupi.Jr': (60, 80),  # Rotational forward
    'Van Hecke': (50, 42)   # Central CB
}

def main():
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_facecolor('#1e5d2b') # Dark Pitch Green
    
    # Draw pitch lines
    plt.plot([0, 100], [0, 0], 'white', lw=2)
    plt.plot([0, 100], [100, 100], 'white', lw=2)
    plt.plot([0, 0], [0, 100], 'white', lw=2)
    plt.plot([100, 100], [0, 100], 'white', lw=2)
    plt.plot([0, 100], [50, 50], 'white', lw=1)
    center_circle = plt.Circle((50, 50), 10, color='white', fill=False, lw=1)
    ax.add_artist(center_circle)
    
    # Goal areas
    ax.add_patch(patches.Rectangle((25, 0), 50, 10, fill=False, color='white', lw=1, alpha=0.5))
    ax.add_patch(patches.Rectangle((25, 90), 50, 10, fill=False, color='white', lw=1, alpha=0.5))

    starters = [
        "Raya", "Gabriel", "J.Timber", "Muñoz", "Alderete",
        "Mbeumo", "B.Fernandes", "Rogers", "Semenyo",
        "Haaland", "Calvert-Lewin"
    ]

    for name in starters:
        x, y = COORDINATES.get(name, (50, 50))
        
        # Plot
        color = 'gold' if name == 'Gabriel' else '#00BFFF' # TC Gold vs Deep Sky Blue
        ax.scatter(x, y, s=1000, color=color, edgecolors='black', zorder=5)
        
        # Label
        label = name
        if name == 'Gabriel': label += "\n[TC]"
        
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black')

    # Connections (Tactical Structure)
    # Defense
    plt.plot([COORDINATES['Alderete'][0], COORDINATES['Gabriel'][0], COORDINATES['J.Timber'][0]], 
             [COORDINATES['Alderete'][1], COORDINATES['Gabriel'][1], COORDINATES['J.Timber'][1]], 
             'white', alpha=0.3, ls='--', zorder=2)
    
    # Attack
    plt.plot([COORDINATES['Semenyo'][0], COORDINATES['Haaland'][0], COORDINATES['Mbeumo'][0]], 
             [COORDINATES['Semenyo'][1], COORDINATES['Haaland'][1], COORDINATES['Mbeumo'][1]], 
             'white', alpha=0.3, ls='--', zorder=2)

    plt.title(f"GW26 ACTUAL AVERAGE POSITIONS\n(In-Match Data Integration)", color='white', fontsize=16, pad=20)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#1e5d2b')
    print(f"Actual Position Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
