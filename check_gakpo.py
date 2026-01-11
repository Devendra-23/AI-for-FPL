import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']
teams = {t['id']: t['short_name'] for t in data['teams']}

targets = ["Gakpo", "Mukiele", "Haaland", "Alderete", "Tavernier"]

for p in elements:
    name = p['web_name']
    for t in targets:
        if t.lower() in name.lower():
            print(f"{name} ({teams[p['team']]}): £{p['now_cost']/10}m Form: {p['form']}")

# Double check Gakpo specifically
