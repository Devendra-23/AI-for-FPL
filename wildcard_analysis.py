import requests
import json
from datetime import datetime

# 1. Fetch Bootstrap Static (Players, Teams, Settings)
url_bootstrap = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = requests.get(url_bootstrap).json()

elements = data['elements']
teams = data['teams']
events = data['events']

# Map team IDs to names and short names
team_map = {t['id']: {'name': t['name'], 'short': t['short_name']} for t in teams}

# 2. Fetch Fixtures
url_fixtures = "https://fantasy.premierleague.com/api/fixtures/"
fixtures = requests.get(url_fixtures).json()

# Filter fixtures for upcoming Gameweeks (e.g., GW 22 to 27)
upcoming_gws = [22, 23, 24, 25, 26, 27]
team_fixtures = {id: [] for id in team_map.keys()}

for f in fixtures:
    if f['event'] in upcoming_gws:
        home_team = f['team_h']
        away_team = f['team_a']
        difficulty_h = f['team_h_difficulty']
        difficulty_a = f['team_a_difficulty']
        
        team_fixtures[home_team].append({'opp': team_map[away_team]['short'], 'diff': difficulty_h, 'loc': 'H'})
        team_fixtures[away_team].append({'opp': team_map[home_team]['short'], 'diff': difficulty_a, 'loc': 'A'})

# Calculate FDR (Fixture Difficulty Rating) for next 5 matches
team_fdr = {}
for tid, fixs in team_fixtures.items():
    # Sort by GW (implicit in list order usually, but good to be safe if event was available)
    # Just take first 5
    next_5 = fixs[:5]
    avg_diff = sum(f['diff'] for f in next_5) / len(next_5) if next_5 else 5
    team_fdr[tid] = avg_diff

# 3. Filter Top Players by Position
def get_best_players(position_id, max_price=15.0, min_points=50, sort_by='form'):
    # position_id: 1=GK, 2=DEF, 3=MID, 4=FWD
    candidates = []
    for p in elements:
        if p['element_type'] == position_id and (p['now_cost']/10) <= max_price:
            # Check availability (status != 'u' or 'i' if strictly filtering, but 'd' is doubt)
             if p['status'] not in ['u', 'i', 'n']: 
                candidates.append({
                    'name': p['web_name'],
                    'team': team_map[p['team']]['short'],
                    'team_id': p['team'],
                    'price': p['now_cost'] / 10,
                    'points': p['total_points'],
                    'form': float(p['form']),
                    'ict': float(p['ict_index']),
                    'selected': float(p['selected_by_percent'])
                })
    
    # Sort
    if sort_by == 'form':
        candidates.sort(key=lambda x: x['form'], reverse=True)
    elif sort_by == 'points':
        candidates.sort(key=lambda x: x['points'], reverse=True)
    elif sort_by == 'value':
        candidates.sort(key=lambda x: x['points']/x['price'], reverse=True)
        
    return candidates[:15] # Return top 15

# Get Top Picks
print("--- BEST FIXTURES (Lowest FDR next 5) ---")
sorted_fdr = sorted(team_fdr.items(), key=lambda x: x[1])
for tid, fdr in sorted_fdr[:8]:
    print(f"{team_map[tid]['name']}: {fdr:.2f}")

print("\n--- TOP GKs ---")
for p in get_best_players(1, max_price=6.0, min_points=40):
    print(f"{p['name']} ({p['team']}) £{p['price']} | Form: {p['form']} | Pts: {p['points']}")

print("\n--- TOP DEFs ---")
for p in get_best_players(2, max_price=8.0, min_points=40):
    print(f"{p['name']} ({p['team']}) £{p['price']} | Form: {p['form']} | Pts: {p['points']}")

print("\n--- TOP MIDs ---")
for p in get_best_players(3, max_price=14.0, min_points=50):
    print(f"{p['name']} ({p['team']}) £{p['price']} | Form: {p['form']} | Pts: {p['points']}")

print("\n--- TOP FWDs ---")
for p in get_best_players(4, max_price=15.0, min_points=40):
    print(f"{p['name']} ({p['team']}) £{p['price']} | Form: {p['form']} | Pts: {p['points']}")
