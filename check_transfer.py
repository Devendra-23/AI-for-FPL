import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

targets = ["Cunha", "Enzo"]
found = []

for p in elements:
    name = p['web_name']
    for t in targets:
        if t.lower() in name.lower():
             print(f"{name}: £{p['now_cost']/10}m Form: {p['form']} Status: {p['status']} Team ID: {p['team']}")
