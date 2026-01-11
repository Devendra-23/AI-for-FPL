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

targets = ["Milenkovi"]
found = []

defenders_under_44 = []

for p in elements:
    web_name = p['web_name']
    
    # Check for targets
    for t in targets:
        if t.lower() in web_name.lower():
            team = get_team_name(p['team'])
            price = p['now_cost'] / 10.0
            found.append(f"{p['web_name']} ({team}): £{price}m")
            
    # Check for cheap defenders
    if p['element_type'] == 2 and p['now_cost'] <= 44:
         team = get_team_name(p['team'])
         price = p['now_cost'] / 10.0
         # Filter for likely starters (total_points > 30 or mins > 500)
         if p['total_points'] > 30:
             defenders_under_44.append(f"{web_name} ({team}) £{price}m Pts:{p['total_points']}")

for f in found:
    print(f)

print("\nDefenders <= 4.4m (selected):")
# Sort by points
defenders_under_44.sort(key=lambda x: int(x.split('Pts:')[1]), reverse=True)
for d in defenders_under_44[:10]:
    print(d)
