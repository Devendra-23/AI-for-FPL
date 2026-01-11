import requests

data = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
teams = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()['teams']
team_map = {t['id']: t['short_name'] for t in teams}

# IDs: CHE=7, WOL=20 (Wait, let me verify WOL ID from previous output. Previous output said Cunha Team ID: 14. Wait. 
# Let's map IDs dynamically to be safe).

# Re-fetch boostrap to map ID to Name
bootstrap = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
team_dict = {t['id']: t['short_name'] for t in bootstrap['teams']}

che_id = 7 # From previous output
wol_id = 0 # Need to find

for tid, name in team_dict.items():
    if name == "WOL":
        wol_id = tid
    if name == "CHE":
        che_id = tid

print(f"CHE ID: {che_id}, WOL ID: {wol_id}")

print(f"\n--- CHELSEA FIXTURES (Next 5) ---")
count = 0
for f in data:
    if f['event'] and f['event'] >= 22:
        if f['team_h'] == che_id:
            print(f"GW{f['event']}: vs {team_dict[f['team_a']]} (H) Diff: {f['team_h_difficulty']}")
            count += 1
        elif f['team_a'] == che_id:
            print(f"GW{f['event']}: vs {team_dict[f['team_h']]} (A) Diff: {f['team_a_difficulty']}")
            count += 1
        if count >= 5: break

print(f"\n--- WOLVES FIXTURES (Next 5) ---") # Wait, Cunha is Team ID 14. Which team is 14?
print(f"Checking Team 14: {team_dict[14]}")

# Let's print fixtures for Team 14 (Cunha's Team)
count = 0
for f in data:
    if f['event'] and f['event'] >= 22:
        if f['team_h'] == 14:
            print(f"GW{f['event']}: vs {team_dict[f['team_a']]} (H) Diff: {f['team_h_difficulty']}")
            count += 1
        elif f['team_a'] == 14:
            print(f"GW{f['event']}: vs {team_dict[f['team_h']]} (A) Diff: {f['team_a_difficulty']}")
            count += 1
        if count >= 5: break
