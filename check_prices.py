import requests
import json

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()
elements = data['elements']
teams = data['teams']

def get_team_name(id):
    for t in teams:
        if t['id'] == id:
            return t['short_name']
    return str(id)

targets = ["Thiago", "Robinson", "Milenkovic", "Evanilson"]
found = []

for p in elements:
    web_name = p['web_name']
    # Check for partial matches or exact
    for t in targets:
        if t.lower() in web_name.lower():
            team = get_team_name(p['team'])
            price = p['now_cost'] / 10.0
            found.append(f"{p['web_name']} ({team}): £{price}m")

for f in found:
    print(f)
