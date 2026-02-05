import json
import requests

# Fetch data from API
data_fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
data_bootstrap = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()

teams = {t['id']: t['short_name'] for t in data_bootstrap['teams']}
target_teams = [3, 17, 11, 4] # BUR, SUN, LEE, BOU

print("--- GW26 FIXTURES for BENCH ---")
for fixture in data_fixtures:
    if fixture['event'] == 26:
        h = fixture['team_h']
        a = fixture['team_a']
        if h in target_teams or a in target_teams:
            print(f"{teams[h]} vs {teams[a]}")

print("\n--- UPCOMING DOUBLES/BLANKS (GW25-38) ---")
# Count fixtures per gameweek for these teams
counts = {}
for t_id in target_teams:
    counts[t_id] = {}

for fixture in data_fixtures:
    if fixture['event'] and fixture['event'] >= 25:
        gw = fixture['event']
        for t_id in target_teams:
            if fixture['team_h'] == t_id or fixture['team_a'] == t_id:
                counts[t_id][gw] = counts[t_id].get(gw, 0) + 1

for t_id in target_teams:
    print(f"\nTeam: {teams[t_id]}")
    for gw, count in sorted(counts[t_id].items()):
        if count != 1:
            print(f"  GW{gw}: {count} fixtures (Blank/Double)")
