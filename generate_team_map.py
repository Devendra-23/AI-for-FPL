import json
import csv
import urllib.request
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Configuration
USER_ID = 17339 # Dev
GW = 21
CSV_FILE = 'Dev_Player_Performance.csv'
JSON_FILE = 'fpl_data.json'
OUTPUT_IMAGE = 'Dev_Team_Map_GW21.png'

# Position Mapping
POSITIONS = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}

def fetch_json(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_recent_stats_from_csv(player_name):
    """Reads the CSV to find the most recent xG/xA stats for a player."""
    if not os.path.exists(CSV_FILE):
        return None
    
    stats = {'xG': '0.00', 'xA': '0.00', 'Pts': '0'}
    
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, [])
        # Find latest GW columns
        # Header format: Name, GW19_Status, GW19_Min, ...
        # We look for the highest GW number
        
        # Identify relevant columns for the latest GW found in header
        latest_gw = 0
        xg_idx = -1
        xa_idx = -1
        pts_idx = -1
        
        for i, col in enumerate(header):
            if "_xG" in col:
                gw_num = int(col.split('_')[0].replace('GW', ''))
                if gw_num > latest_gw:
                    latest_gw = gw_num
        
        if latest_gw > 0:
            xg_col = f"GW{latest_gw}_xG"
            xa_col = f"GW{latest_gw}_xA"
            pts_col = f"GW{latest_gw}_Pts"
            
            try:
                xg_idx = header.index(xg_col)
                xa_idx = header.index(xa_col)
                pts_idx = header.index(pts_col)
            except ValueError:
                pass

        for row in reader:
            if row[0] == player_name:
                if xg_idx != -1 and len(row) > xg_idx:
                    stats['xG'] = row[xg_idx]
                    stats['xA'] = row[xa_idx]
                    stats['Pts'] = row[pts_idx]
                return stats
    return stats

def main():
    # 1. Load Static Data
    print("Loading FPL Data...")
    try:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
        elements = data['elements']
    except Exception as e:
        print(f"Failed to load {JSON_FILE}: {e}")
        return

    # 2. Fetch Picks
    print(f"Fetching Picks for GW{GW}...")
    url = f"https://fantasy.premierleague.com/api/entry/{USER_ID}/event/{GW}/picks/"
    picks_data = fetch_json(url)
    if not picks_data:
        print("Could not fetch picks. Is the game updating or ID wrong?")
        # Fallback to previous GW if GW21 not available
        url = f"https://fantasy.premierleague.com/api/entry/{USER_ID}/event/{GW-1}/picks/"
        print(f"Trying GW{GW-1}...")
        picks_data = fetch_json(url)
        if not picks_data: return

    active_picks = picks_data['picks']
    
    # 3. Organize Players by Position
    team = {'GKP': [], 'DEF': [], 'MID': [], 'FWD': [], 'Bench': []}
    
    for pick in active_picks:
        pid = pick['element']
        multiplier = pick['multiplier']
        is_starter = multiplier > 0
        
        # Find player details
        p_data = next((p for p in elements if p['id'] == pid), None)
        if not p_data: continue
        
        name = p_data['web_name']
        pos_id = p_data['element_type']
        pos_str = POSITIONS[pos_id]
        
        # Get extra stats
        csv_stats = get_recent_stats_from_csv(name)
        
        # Combine info
        player_info = {
            'name': name,
            'pos': pos_str,
            'form': p_data['form'],
            'price': p_data['now_cost'] / 10,
            'xG': csv_stats['xG'] if csv_stats else '-',
            'xA': csv_stats['xA'] if csv_stats else '-',
            'last_pts': csv_stats['Pts'] if csv_stats else '-',
            'is_capt': pick['is_captain'],
            'is_vice': pick['is_vice_captain']
        }
        
        if is_starter:
            team[pos_str].append(player_info)
        else:
            team['Bench'].append(player_info)

    # 4. Draw Pitch
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_facecolor('#2E8B57') # Pitch Green

    # Draw Pitch Markings (Simplified)
    plt.plot([0, 100], [50, 50], 'white', alpha=0.3) # Center Line
    circle = plt.Circle((50, 50), 10, color='white', fill=False, alpha=0.3)
    ax.add_artist(circle)
    
    # Define Layout Zones (Y coordinates)
    # GKP: 10, DEF: 30, MID: 60, FWD: 85
    zones = {
        'GKP': 10,
        'DEF': 30,
        'MID': 60,
        'FWD': 85
    }
    
    # Plot Starters
    for pos, players in team.items():
        if pos == 'Bench': continue
        
        y = zones[pos]
        count = len(players)
        if count == 0: continue
        
        # Calculate X coordinates to center them
        # Space them out evenly between 10 and 90
        spacing = 100 / (count + 1)
        
        for i, p in enumerate(players):
            x = spacing * (i + 1)
            
            # Label
            label = f"{p['name']}"
            if p['is_capt']: label += " (C)"
            elif p['is_vice']: label += " (V)"
            
            stats_text = f"Form: {p['form']}\nLast xG: {p['xG']}\nLast xA: {p['xA']}"
            
            # Plot Dot
            ax.plot(x, y, 'bo', markersize=15, color='white', markeredgecolor='black')
            
            # Plot Text
            ax.text(x, y-2, label, ha='center', va='top', fontsize=10, fontweight='bold', color='white')
            ax.text(x, y-5, stats_text, ha='center', va='top', fontsize=8, color='yellow')

    # Plot Bench
    ax.text(50, -5, "BENCH", ha='center', fontsize=12, fontweight='bold', color='white')
    bench_count = len(team['Bench'])
    if bench_count > 0:
        spacing = 100 / (bench_count + 1)
        for i, p in enumerate(team['Bench']):
            x = spacing * (i + 1)
            y = -10 # Below the pitch
            
            label = f"{p['name']}"
            stats_text = f"Form: {p['form']}"
            
            ax.plot(x, y, 'bo', markersize=10, color='gray', markeredgecolor='white')
            ax.text(x, y-2, label, ha='center', va='top', fontsize=9, color='white')
            ax.text(x, y-4, stats_text, ha='center', va='top', fontsize=7, color='lightgray')

    ax.set_xlim(0, 100)
    ax.set_ylim(-20, 100)
    ax.axis('off') # Hide axes
    
    plt.title(f"Team Map - GW{GW}", color='black', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=100, bbox_inches='tight')
    print(f"Map generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
