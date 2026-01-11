import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
for p in data['elements']:
    if "Lewis Hall" in p['web_name'] or "Hall" in p['web_name']:
        team = data['teams'][p['team']-1]['short_name']
        print(f"{p['web_name']} ({team}): £{p['now_cost']/10} Form: {p['form']}")
