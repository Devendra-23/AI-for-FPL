import requests
import json
import sys

league_id = 17291
url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    print(f"League: {data['league']['name']}")
    print(f"| Rank | Team | Manager | ID | Total | GW |")
    print("|---|---|---|---|---|---|")
    
    for r in data['standings']['results'][:20]:
        print(f"| {r['rank']} | {r['entry_name']} | {r['player_name']} | {r['entry']} | {r['total']} | {r['event_total']} |")

except Exception as e:
    print(f"Error fetching standings: {e}")
