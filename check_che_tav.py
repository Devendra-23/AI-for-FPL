import requests

# Fetch Data
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']
teams = {t['id']: t['short_name'] for t in data['teams']}

print(f"{ 'NAME':<20} {'TEAM':<5} {'PRICE':<5} {'FORM':<5} {'PTS':<5} {'MINS':<5} {'STATUS'}")
print("-" * 65)

# Check Tavernier
found_tav = False
for p in elements:
    if "Tavernier" in p['web_name']:
        team = teams[p['team']]
        print(f"{p['web_name']:<20} {team:<5} £{p['now_cost']/10:<4} {p['form']:<5} {p['total_points']:<5} {p['minutes']:<5} {p['status']}")
        found_tav = True

if not found_tav:
    print("Tavernier not found.")

print("\n--- CHELSEA ASSETS (Sorted by Form) ---")
che_players = []
for p in elements:
    if teams[p['team']] == "CHE":
        che_players.append(p)

# Sort by Form
che_players.sort(key=lambda x: float(x['form']), reverse=True)

for p in che_players[:15]:
     print(f"{p['web_name']:<20} CHE   £{p['now_cost']/10:<4} {p['form']:<5} {p['total_points']:<5} {p['minutes']:<5} {p['status']}")
