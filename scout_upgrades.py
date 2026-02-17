import json
import csv

def get_position(element_type):
    if element_type == 1: return "GK"
    if element_type == 2: return "DEF"
    if element_type == 3: return "MID"
    if element_type == 4: return "FWD"
    return "?"

def scout():
    with open('fpl_data.json', 'r') as f:
        data = json.load(f)
    
    players = data['elements']
    teams = {t['id']: t['name'] for t in data['teams']}
    
    # Filter for players with good form or high xG+xA in recent weeks
    # For scouting, we look for players who are NOT in the current team or are upgrades
    current_team_names = ["Raya", "Gabriel", "Timber", "Alderete", "Van Hecke", "Mbeumo", "Fernandes", "Semenyo", "Enzo", "Rogers", "Haaland", "Calvert-Lewin"]
    
    scouted = []
    
    for p in players:
        # Metrics: form > 5 or (xG + xA) per match > 0.4
        form = float(p['form'])
        xg = float(p['expected_goals'])
        xa = float(p['expected_assists'])
        
        # Simple score for potential
        score = form * 0.5 + (xg + xa) * 0.5
        
        if (form > 6.0 or score > 10) and p['web_name'] not in current_team_names:
            scouted.append({
                'name': p['web_name'],
                'team': teams[p['team']],
                'pos': get_position(p['element_type']),
                'cost': p['now_cost'] / 10,
                'form': form,
                'xG': xg,
                'xA': xa,
                'pts': p['total_points'],
                'score': score
            })
            
    # Sort by score
    scouted.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"{'Name':<18} | {'Team':<15} | {'Pos':<4} | {'Cost':<5} | {'Form':<5} | {'xG+xA':<6}")
    print("-" * 65)
    for p in scouted[:15]:
        print(f"{p['name']:<18} | {p['team']:<15} | {p['pos']:<4} | £{p['cost']:<4} | {p['form']:<5} | {p['xG']+p['xA']:<6.2f}")

if __name__ == "__main__":
    scout()
