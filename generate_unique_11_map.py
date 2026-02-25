import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'Dev_Unique_11_Roadmap.png'

# Dev's Proposed UNIQUE 11 Squad
UNIQUE_SQUAD = [
    {'name': 'Raya', 'pos': (50, 10), 'color': '#ef0107', 'team': 'Arsenal'},
    {'name': 'Virgil', 'pos': (50, 32), 'color': '#e32221', 'team': 'Liverpool'},
    {'name': 'Murillo', 'pos': (30, 28), 'color': '#ce1126', 'team': 'NFO'},
    {'name': 'Hill', 'pos': (70, 28), 'color': '#af122a', 'team': 'BOU'},
    {'name': 'Bruno F.', 'pos': (55, 65), 'color': '#DA291C', 'team': 'Man Utd'},
    {'name': 'Semenyo', 'pos': (82, 60), 'color': '#6CABDD', 'team': 'Man City'},
    {'name': 'Bowen', 'pos': (85, 75), 'color': '#7A263A', 'team': 'West Ham'},
    {'name': 'Palmer', 'pos': (15, 75), 'color': '#034694', 'team': 'Chelsea'},
    {'name': 'Rogers', 'pos': (30, 65), 'color': '#95BFE5', 'team': 'Aston Villa'},
    {'name': 'Haaland', 'pos': (52, 88), 'color': '#6CABDD', 'team': 'Man City'},
    {'name': 'Thiago', 'pos': (45, 82), 'color': '#e30613', 'team': 'Brentford'},
    {'name': 'Gordon', 'pos': (65, 82), 'color': '#241f20', 'team': 'Newcastle'}
]

def main():
    fig, ax = plt.subplots(figsize=(14, 16))
    ax.set_facecolor('#eef7ee')
    
    # Pitch Markings
    plt.plot([0, 100], [0, 0], '#444444', lw=2)
    plt.plot([0, 100], [100, 100], '#444444', lw=2)
    plt.plot([0, 100], [50, 50], '#444444', lw=1, alpha=0.3)
    center_circle = plt.Circle((50, 50), 10, color='#444444', fill=False, lw=1, alpha=0.3)
    ax.add_artist(center_circle)

    for p in UNIQUE_SQUAD:
        x, y = p['pos']
        ax.scatter(x, y, s=2000, color=p['color'], edgecolors='black', linewidth=2, zorder=5)
        # Handle text color for dark backgrounds
        text_color = 'white' if p['team'] in ['Newcastle', 'West Ham', 'Chelsea', 'NFO'] else 'black'
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color=text_color)
        
        # Team Label
        ax.text(x, y-7, p['team'], ha='center', va='top', fontsize=8, color='black', 
                fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2'))

    plt.title("DEV: THE UNIQUE 11 ROADMAP\n1 Player per Elite Team Strategy | GW31 Optimized", 
              color='black', fontsize=20, fontweight='bold', pad=40)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
