import matplotlib.pyplot as plt

# Configuration
OUTPUT_IMAGE = 'UCL_Playoff_Tactical_Map.png'

# UCL Playoff Top Targets (Positions & Stats)
TARGETS = [
    {'name': 'Mbappé', 'pos': (52, 88), 'color': '#ffffff', 'team': 'Real Madrid', 'stats': 'xG: 8.2 | Pts: 48'},
    {'name': 'Lautaro', 'pos': (48, 80), 'color': '#0066b2', 'team': 'Inter Milan', 'stats': 'xG: 6.5 | Pts: 41'},
    {'name': 'Bellingham', 'pos': (70, 70), 'color': '#ffffff', 'team': 'Real Madrid', 'stats': 'xGI: 7.1 | Pts: 44'},
    {'name': 'Xavi Simons', 'pos': (30, 72), 'color': '#e32221', 'team': 'Leverkusen', 'stats': 'xG: 4.0 | xA: 5.0'},
    {'name': 'Barcola', 'pos': (85, 75), 'color': '#004170', 'team': 'PSG', 'stats': 'xG: 6.0 | Pts: 42'},
    {'name': 'Hakimi', 'pos': (88, 55), 'color': '#004170', 'team': 'PSG', 'stats': 'xA: 3.2 | Pts: 38'},
    {'name': 'Dimarco', 'pos': (12, 60), 'color': '#0066b2', 'team': 'Inter Milan', 'stats': 'xA: 4.1 | Pts: 42'},
    {'name': 'Grimaldo', 'pos': (15, 50), 'color': '#e32221', 'team': 'Leverkusen', 'stats': 'xA: 3.5 | Pts: 35'},
    {'name': 'Hall', 'pos': (22, 40), 'color': '#241f20', 'team': 'Newcastle', 'stats': 'xGC: 0.8 | Pts: 31'},
    {'name': 'Raya', 'pos': (50, 10), 'color': '#ef0107', 'team': 'Arsenal*', 'stats': 'CS: 5 | Pts: 45'} # Note: Arsenal 1st, but Raya as high-end template benchmark
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

    for p in TARGETS:
        x, y = p['pos']
        ax.scatter(x, y, s=1800, color=p['color'], edgecolors='black', linewidth=1.5, zorder=5)
        ax.text(x, y, p['name'], ha='center', va='center', fontsize=9, fontweight='bold', zorder=6, color='black' if p['color'] != '#241f20' else 'white')
        
        # Stats Label
        stats_str = f"{p['team']}\n{p['stats']}"
        ax.text(x, y-7, stats_str, ha='center', va='top', fontsize=8, color='white', 
                fontweight='bold', bbox=dict(facecolor='#1a1a1a', alpha=0.9, boxstyle='round,pad=0.3'))

    plt.title("UCL 2025/26 PLAYOFFS: TACTICAL TARGET MAP\nHigh-Performance Assets from Teams 9-24", 
              color='black', fontsize=18, fontweight='bold', pad=30)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    plt.savefig(OUTPUT_IMAGE, dpi=120, bbox_inches='tight', facecolor='#eef7ee')
    print(f"UCL Playoff Map Generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
