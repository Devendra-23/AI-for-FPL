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

def update_player_performance_csv(filename, gw, player_stats_list):
    """Saves granular player-by-player stats to a separate CSV."""
    # Append suffix to user's main CSV name or use a dedicated one
    player_filename = filename.replace('Performance_Tracker.csv', 'Player_Performance.csv')
    
    file_exists = os.path.exists(player_filename)
    
    with open(player_filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Gameweek", "Name", "Status", "Min", "Pts", "xG", "xA", "xGC", "G", "A", "CS"])
        
        for p in player_stats_list:
            writer.writerow([gw] + p)
    print(f"Detailed player stats saved to {player_filename}")

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
    print(f"{'Name':<20} | {'Min':<5} | {'Pts':<5} | {'xG':<5} | {'xA':<5} | {'xGc':<5} | {'G':<3} | {'A':<3} | {'CS':<3}")
    print("-" * 80)

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

            print(f"{name:<16} {status_symbol:<5} | {gw_stats['minutes']:<5} | {pts:<5} | {xg:<5.2f} | {xa:<5.2f} | {xgc:<5.2f} | {gw_stats['goals_scored']:<3} | {gw_stats['assists']:<3} | {gw_stats['clean_sheets']:<3}")
            
            # Add to list for CSV saving
            player_stats_to_save.append([
                name, status_symbol, gw_stats['minutes'], pts, 
                f"{xg:.2f}", f"{xa:.2f}", f"{xgc:.2f}", 
                gw_stats['goals_scored'], gw_stats['assists'], gw_stats['clean_sheets']
            ])
        else:
            print(f"{name:<20} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<3} | {'-':<3} | {'-':<3}")
        
        time.sleep(0.05)

    print("-" * 80)
    print(f"TEAM TOTALS (Active) |       | {team_total_points:<5} | {team_total_xg:<5.2f} | {team_total_xa:<5.2f} | {team_total_xgc:<5.2f} |     |     |    ")
    
    update_tracker_csv(csv_file, args.gw, team_total_points, team_total_xg, team_total_xa, team_total_xgc)
    update_player_performance_csv(csv_file, args.gw, player_stats_to_save)

if __name__ == "__main__":
    main()
