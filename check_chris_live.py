import requests
import json

# Config
chris_id = 4669858
gw = 25

# Fetch Picks
picks_url = f"https://fantasy.premierleague.com/api/entry/{chris_id}/event/{gw}/picks/"
picks_data = requests.get(picks_url).json()
picks = {p['element']: p for p in picks_data['picks']}

# Fetch Static Data (Players)
static_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
static_data = requests.get(static_url).json()
elements = {e['id']: e for e in static_data['elements']}
teams = {t['id']: t['name'] for t in static_data['teams']}

# Fetch Live Points
live_url = f"https://fantasy.premierleague.com/api/event/{gw}/live/"
live_data = requests.get(live_url).json()
live_elements = {e['id']: e['stats'] for e in live_data['elements']}

print(f"Chris's GW{gw} Performance")
print(f"Active Chip: {picks_data.get('active_chip')}")
print("-" * 60)
print(f"{'Player':<20} | {'Team':<10} | {'Pts':<5} | {'Status'}")
print("-" * 60)

total_score = 0

for pid, pick_info in picks.items():
    player = elements[pid]
    stats = live_elements.get(pid, {'total_points': 0})
    pts = stats['total_points']
    
    # Handle Captaincy
    if pick_info['is_captain']:
        pts *= pick_info['multiplier']
        name = f"{player['web_name']} (C)"
    elif pick_info['is_vice_captain']:
        name = f"{player['web_name']} (VC)"
    else:
        name = player['web_name']
        
    # Bench
    if pick_info['position'] > 11:
        status = "BENCH"
    else:
        status = "PLAYING"
        total_score += pts
        
    print(f"{name:<20} | {teams[player['team']]:<10} | {pts:<5} | {status}")

print("-" * 60)
print(f"Projected Total: {total_score}")
