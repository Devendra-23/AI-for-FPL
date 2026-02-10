import requests
import json

def fetch_adam_team():
    entry_id = 7456922
    gw = 24  # Fetching the Pre-FH team
    
    # Picks
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gw}/picks/"
    response = requests.get(url).json()
    picks = response['picks']
    bank = response['entry_history']['bank'] / 10
    
    # Static Data
    static = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    players = {p['id']: p for p in static['elements']}
    teams = {t['id']: t['name'] for t in static['teams']}
    
    print(f"Adam's Squad (GW{gw} Snapshot)")
    print(f"Bank: £{bank}m")
    print("-" * 50)
    
    pos_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    
    for p in picks:
        player = players[p['element']]
        team = teams[player['team']]
        pos = pos_map[player['element_type']]
        cost = player['now_cost'] / 10
        print(f"{player['web_name']:<15} | {team:<10} | {pos:<3} | £{cost}m")

if __name__ == "__main__":
    fetch_adam_team()
