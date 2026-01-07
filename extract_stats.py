import json

def get_position(element_type):
    if element_type == 1: return "GK"
    if element_type == 2: return "DEF"
    if element_type == 3: return "MID"
    if element_type == 4: return "FWD"
    return "?"

with open('fpl_data.json', 'r') as f:
    data = json.load(f)

players = data['elements']
teams = {t['id']: t['short_name'] for t in data['teams']}

targets = [
    "Alderete",
    "Gudmundsson",
    "Devenny",
    "Hecke",
    "Cunha",
    "Calvert-Lewin",
    "Dúbravka",
    "Dubravka"
]

print(f"{'Name':<20} | {'Team':<5} | {'Pos':<5} | {'Cost':<5} | {'Pts':<5} | {'Form':<5} | {'xG':<5} | {'xA':<5} | {'xGc':<5} | {'CS':<3} | {'Min':<5} | {'G':<3} | {'A':<3}")
print("-" * 125)

found_ids = []

for p in players:
    name_match = any(t.lower() in p['web_name'].lower() or t.lower() in p['second_name'].lower() for t in targets)
    
    if name_match:
        # Special check for Gudmundsson to avoid wrong ones if multiple
        if "Gudmundsson" in p['web_name'] and p['team'] not in [teams.keys()]:
            pass 

        team_name = teams.get(p['team'], str(p['team']))
        pos = get_position(p['element_type'])
        cost = p['now_cost'] / 10.0
        
        print(f"{p['web_name']:<20} | {team_name:<5} | {pos:<5} | £{cost}m | {p['total_points']:<5} | {p['form']:<5} | {p['expected_goals']:<5} | {p['expected_assists']:<5} | {p['expected_goals_conceded']:<5} | {p['clean_sheets']:<3} | {p['minutes']:<5} | {p['goals_scored']:<3} | {p['assists']:<3}")
