import requests

data = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
bootstrap = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
team_dict = {t['id']: t['short_name'] for t in bootstrap['teams']}

print("--- GW25 FIXTURES ---")
for f in data:
    if f['event'] == 25:
        h_name = team_dict[f['team_h']]
        a_name = team_dict[f['team_a']]
        print(f"{h_name} vs {a_name}")
