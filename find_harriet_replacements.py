import json
import sys

def get_replacements():
    try:
        with open('fpl_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: fpl_data.json not found.")
        return

    elements = data['elements']
    
    # O'Reilly Stats
    target_price = 5.3
    
    print("SEARCHING FOR MIDFIELDERS (MID) | Price: <= £5.5m | Better than O'Reilly")
    print("-" * 75)
    print(f"{'Name':<20} | {'Team':<4} | {'Price':<6} | {'Form':<5} | {'Pts':<4} | {'ICT':<5} | {'Next 3 Fixtures'}")
    print("-" * 75)

    replacements = []
    
    for p in elements:
        # Filter for Midfielders (Element Type 3)
        if p['element_type'] != 3:
            continue
            
        # Price Range: <= £5.5m
        price = p['now_cost'] / 10
        if price > 5.5:
            continue
            
        # Filter dead wood / low form
        # O'Reilly has form 0.0-ish and 1pt recently.
        # We want active players.
        if float(p['form']) < 2.5:
            continue
            
        if p['total_points'] < 40:
            continue

        replacements.append(p)

    # Sort by Form descending
    replacements.sort(key=lambda x: float(x['form']), reverse=True)
    
    for r in replacements[:10]:
        print(f"{r['web_name']:<20} | {r['team']:<4} | £{r['now_cost']/10:<5} | {r['form']:<5} | {r['total_points']:<4} | {r['ict_index']:<5} | Check Team {r['team']}")

if __name__ == "__main__":
    get_replacements()
