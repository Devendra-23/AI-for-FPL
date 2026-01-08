import json
import urllib.request
import sys
import time
import ssl
import csv
import os
import argparse

# Configuration for Users
USERS = {
    'dev': {
        'id': 17339,
        'csv': 'Dev_Performance_Tracker.csv'
    },
    'harriet': {
        'id': 2610341,
        'csv': 'Harriet_Performance_Tracker.csv'
    },
    'chris': {
        'id': 4669858,
        'csv': 'Chris_Performance_Tracker.csv'
    }
}

def fetch_json(url):
    """Helper to fetch JSON from URL with SSL bypass."""
    # Create an unverified context to avoid SSL errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url)
        # Add User-Agent to avoid 403 Forbidden on some endpoints
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching {url}: {e.code} {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_team_picks(team_id, gw):
    """Fetches the players picked by the team for a specific gameweek."""
    url = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{gw}/picks/"
    data = fetch_json(url)
    if data and 'picks' in data:
        return data['picks']
    return []

def fetch_player_details(player_id, players_static_data):
    """Gets basic player info (Name, Team, Pos) from the static bootstrap data."""
    for p in players_static_data:
        if p['id'] == player_id:
            return p
    return None

def fetch_player_history(player_id):
    """Fetches detailed history for a specific player."""
    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    return fetch_json(url)

def update_player_performance_csv_horizontal(filename, gw, player_stats_list):
    """
    Saves player stats in a horizontal format (Name | GW19_Pts | GW19_xG | ... | GW20_Pts ...).
    Handles migration from old vertical format automatically.
    """
    player_filename = filename.replace('Performance_Tracker.csv', 'Player_Performance.csv')
    
    data_store = {} # { "PlayerName": { gw_int: { "Status": ..., "Min": ... } } }
    all_gws = set()

    # Metrics we track per GW
    metrics = ["Status", "Min", "Pts", "xG", "xA", "xGC", "G", "A", "CS", "Cost"]

    # 1. Read existing data
    if os.path.exists(player_filename):
        with open(player_filename, 'r') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                header = []

            if "Gameweek" in header and "Name" in header:
                # Old Vertical Format detected
                # Header: Gameweek, Name, Status, Min, Pts, xG, xA, xGC, G, A, CS
                try:
                    idx_gw = header.index("Gameweek")
                    idx_name = header.index("Name")
                    # Map other columns
                    col_map = {m: header.index(m) for m in metrics if m in header}
                    
                    for row in reader:
                        if not row: continue
                        p_name = row[idx_name]
                        p_gw = int(row[idx_gw])
                        all_gws.add(p_gw)
                        
                        if p_name not in data_store: data_store[p_name] = {}
                        if p_gw not in data_store[p_name]: data_store[p_name][p_gw] = {}

                        for m, idx in col_map.items():
                            data_store[p_name][p_gw][m] = row[idx]
                except ValueError:
                    print("Warning: Could not parse old vertical CSV format completely.")
            
            elif "Name" in header:
                # New Horizontal Format assumed
                # Header: Name, GW19_Status, GW19_Min, ...
                for row in reader:
                    if not row: continue
                    p_name = row[0]
                    if p_name not in data_store: data_store[p_name] = {}
                    
                    # Parse columns
                    for i, col_name in enumerate(header[1:], 1):
                        if "_" in col_name:
                            parts = col_name.split("_")
                            # Format: GW19_Status
                            if parts[0].startswith("GW"):
                                try:
                                    g_num = int(parts[0].replace("GW", ""))
                                    metric = parts[1]
                                    all_gws.add(g_num)
                                    
                                    if g_num not in data_store[p_name]: data_store[p_name][g_num] = {}
                                    if i < len(row):
                                        data_store[p_name][g_num][metric] = row[i]
                                except ValueError:
                                    pass

    # 2. Merge new data
    # player_stats_list items: [Name, Status, Min, Pts, xG, xA, xGC, G, A, CS, Cost]
    # Indices corresponding to metrics list:
    # Status=1, Min=2, Pts=3, xG=4, xA=5, xGC=6, G=7, A=8, CS=9
    
    current_gw = int(gw)
    all_gws.add(current_gw)
    
    for p in player_stats_list:
        p_name = p[0]
        if p_name not in data_store: data_store[p_name] = {}
        if current_gw not in data_store[p_name]: data_store[p_name][current_gw] = {}
        
        data_store[p_name][current_gw]["Status"] = p[1]
        data_store[p_name][current_gw]["Min"] = p[2]
        data_store[p_name][current_gw]["Pts"] = p[3]
        data_store[p_name][current_gw]["xG"] = p[4]
        data_store[p_name][current_gw]["xA"] = p[5]
        data_store[p_name][current_gw]["xGC"] = p[6]
        data_store[p_name][current_gw]["G"] = p[7]
        data_store[p_name][current_gw]["A"] = p[8]
        data_store[p_name][current_gw]["CS"] = p[9]
        data_store[p_name][current_gw]["Cost"] = p[10]

    # 3. Write back in Horizontal Format
    sorted_gws = sorted(list(all_gws))
    
    # Build Header
    new_header = ["Name"]
    for g in sorted_gws:
        for m in metrics:
            new_header.append(f"GW{g}_{m}")
            
    with open(player_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        
        # Sort players by name for consistency
        for p_name in sorted(data_store.keys()):
            row = [p_name]
            for g in sorted_gws:
                stats = data_store[p_name].get(g, {})
                for m in metrics:
                    row.append(stats.get(m, "-")) # Fill missing with "-"
            writer.writerow(row)

    print(f"Detailed player stats saved to {player_filename} (Horizontal Format)")

def update_tracker_csv(filename, gw, total_points, total_xg, total_xa, total_xgc):
    """Updates the team performance tracker CSV with aggregated stats."""
    
    # Check/Create file if it doesn't exist
    if not os.path.exists(filename):
        print(f"File {filename} not found. Creating new file...")
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Default header for any user
            writer.writerow(["Gameweek","Overall Rank","Gameweek Points","Team Value","Bank","Transfers Made","Chips Used","AI Rating (Hub)","xG","xA","xGC","Clean Sheets (Def)","Captain Points","Bench Points","Notes"])
    
    rows = []
    updated = False
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        
        # Find column indices
        try:
            gw_pts_idx = header.index("Gameweek Points")
            xg_idx = header.index("xG")
            xa_idx = header.index("xA")
            xgc_idx = header.index("xGC")
        except ValueError:
            print("Error: Could not find necessary columns in CSV.")
            return

        for row in reader:
            if row[0] == str(gw):
                # Ensure row is long enough
                while len(row) < len(header):
                    row.append("")
                
                # Update stats
                row[gw_pts_idx] = str(total_points)
                row[xg_idx] = f"{total_xg:.2f}"
                row[xa_idx] = f"{total_xa:.2f}"
                row[xgc_idx] = f"{total_xgc:.2f}"
                updated = True
                print(f"Updated GW{gw} in {filename}: Pts={total_points}, xG={total_xg:.2f}, xA={total_xa:.2f}, xGC={total_xgc:.2f}")
            rows.append(row)
    
    if updated:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    else:
        # If the row for this GW doesn't exist, we append it
        print(f"Adding new row for GW{gw} to {filename}...")
        new_row = [""] * len(header)
        new_row[0] = str(gw)
        new_row[gw_pts_idx] = str(total_points)
        new_row[xg_idx] = f"{total_xg:.2f}"
        new_row[xa_idx] = f"{total_xa:.2f}"
        new_row[xgc_idx] = f"{total_xgc:.2f}"
        rows.append(new_row)
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description='Fetch FPL Gameweek Stats')
    parser.add_argument('gw', type=int, nargs='?', default=20, help='Gameweek number (default: 20)')
    parser.add_argument('--user', type=str, default='dev', choices=['dev', 'harriet', 'chris'], help='User to fetch stats for (dev, harriet, or chris)')
    
    args = parser.parse_args()
    
    user_config = USERS[args.user]
    team_id = user_config['id']
    csv_file = user_config['csv']

    print(f"\nFetching stats for User: {args.user.upper()} (ID: {team_id}), Gameweek {args.gw}...\n")
    print(f"{'Name':<20} | {'Min':<5} | {'Pts':<5} | {'xG':<5} | {'xA':<5} | {'xGc':<5} | {'G':<3} | {'A':<3} | {'CS':<3} | {'Cost'}")
    print("-" * 90)

    # Load static data
    try:
        with open('fpl_data.json', 'r') as f:
            data = json.load(f)
        players_static = data['elements']
    except FileNotFoundError:
        print("Error: 'fpl_data.json' not found. Please run the setup script first.")
        return

    # Fetch Team Picks
    picks = fetch_team_picks(team_id, args.gw)
    
    if not picks:
        print(f"No picks found for GW{args.gw} (or API error).")
        return

    # Aggregators
    team_total_points = 0
    team_total_xg = 0.0
    team_total_xa = 0.0
    team_total_xgc = 0.0
    player_stats_to_save = []
    
    for pick in picks:
        pid = pick['element']
        multiplier = pick['multiplier'] 
        is_starter = multiplier > 0
        
        # Get Player Name
        p_static = fetch_player_details(pid, players_static)
        name = p_static['web_name'] if p_static else str(pid)
        current_cost = p_static['now_cost'] / 10.0 if p_static else 0.0

        # Fetch history
        history_data = fetch_player_history(pid)
        if not history_data:
            continue
            
        # Find the specific gameweek
        gw_stats = next((h for h in history_data['history'] if h['round'] == args.gw), None)
        
        if gw_stats:
            pts = gw_stats['total_points']
            xg = float(gw_stats['expected_goals'])
            xa = float(gw_stats['expected_assists'])
            xgc = float(gw_stats['expected_goals_conceded'])
            
            points_contribution = pts * multiplier
            xg_contribution = xg * (1 if is_starter else 0)
            xa_contribution = xa * (1 if is_starter else 0)
            xgc_contribution = xgc * (1 if is_starter else 0)

            team_total_points += points_contribution
            team_total_xg += xg_contribution
            team_total_xa += xa_contribution
            team_total_xgc += xgc_contribution
            
            status_symbol = "Start" if is_starter else "Bench"
            if multiplier == 2: status_symbol = "Capt"
            if multiplier == 3: status_symbol = "TC"

            print(f"{name:<16} {status_symbol:<5} | {gw_stats['minutes']:<5} | {pts:<5} | {xg:<5.2f} | {xa:<5.2f} | {xgc:<5.2f} | {gw_stats['goals_scored']:<3} | {gw_stats['assists']:<3} | {gw_stats['clean_sheets']:<3} | £{current_cost}m")
            
            # Add to list for CSV saving
            player_stats_to_save.append([
                name, status_symbol, gw_stats['minutes'], pts, 
                f"{xg:.2f}", f"{xa:.2f}", f"{xgc:.2f}", 
                gw_stats['goals_scored'], gw_stats['assists'], gw_stats['clean_sheets'],
                f"{current_cost}"
            ])
        else:
            print(f"{name:<20} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<3} | {'-':<3} | {'-':<3} | £{current_cost}m")
        
        time.sleep(0.05)

    print("-" * 80)
    print(f"TEAM TOTALS (Active) |       | {team_total_points:<5} | {team_total_xg:<5.2f} | {team_total_xa:<5.2f} | {team_total_xgc:<5.2f} |     |     |    ")
    
    update_tracker_csv(csv_file, args.gw, team_total_points, team_total_xg, team_total_xa, team_total_xgc)
    # Use new horizontal update function
    update_player_performance_csv_horizontal(csv_file, args.gw, player_stats_to_save)

if __name__ == "__main__":
    main()
