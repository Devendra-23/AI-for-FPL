import requests
import json

# Fetch Data
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = requests.get(url).json()
elements = data['elements']

# Filter for relevant players
players = []
for p in elements:
    # Active players only
    if p['status'] not in ['u', 'i', 'n']:
        players.append({
            'name': p['web_name'],
            'team': p['team'],
            'pos': p['element_type'],
            'price': p['now_cost'] / 10,
            'sel': float(p['selected_by_percent']),
            'pts': p['total_points'],
            'form': float(p['form']),
            'value': float(p['value_season']),
            'id': p['id']
        })

# Sort by Ownership (Template)
players.sort(key=lambda x: x['sel'], reverse=True)

print("--- TOP 15 TEMPLATE PLAYERS (High Ownership) ---")
for p in players[:15]:
    print(f"{p['name']} ({p['pos']}) £{p['price']} | {p['sel']}% | Pts: {p['pts']} | Form: {p['form']}")

# Sort by Total Points (Performance)
players.sort(key=lambda x: x['pts'], reverse=True)

print("\n--- TOP 15 PERFORMERS (Total Points) ---")
for p in players[:15]:
    print(f"{p['name']} ({p['pos']}) £{p['price']} | {p['sel']}% | Pts: {p['pts']} | Form: {p['form']}")

# Sort by Form (Recent)
players.sort(key=lambda x: x['form'], reverse=True)

print("\n--- TOP 10 FORM PLAYERS (Last 30 Days) ---")
for p in players[:10]:
    print(f"{p['name']} ({p['pos']}) £{p['price']} | {p['sel']}% | Pts: {p['pts']} | Form: {p['form']}")
