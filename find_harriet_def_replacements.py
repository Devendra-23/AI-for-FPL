import json
import sys

def get_def_replacements():
    try:
        with open('fpl_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: fpl_data.json not found.")
        return

    elements = data['elements']
    
    print("SEARCHING FOR DEFENDERS (DEF) | Price: <= £5.5m | Better than O'Reilly")
    print("-" * 75)
    print(f"{'Name':<20} | {'Team':<4} | {'Price':<6} | {'Form':<5} | {'Pts':<4} | {'ICT':<5}")
    print("-" * 75)

    replacements = []
    
    for p in elements:
        # Filter for Defenders (Element Type 2)
        if p['element_type'] != 2:
            continue
            
        # Price Range: <= £5.5m
        price = p['now_cost'] / 10
        if price > 5.5:
            continue
            
        # Filter dead wood
        if float(p['form']) < 3.0:
            continue
            
        if p['total_points'] < 40:
            continue

        replacements.append(p)

    # Sort by Form descending
    replacements.sort(key=lambda x: float(x['form']), reverse=True)
    
    for r in replacements[:10]:
        print(f"{r['web_name']:<20} | {r['team']:<4} | £{r['now_cost']/10:<5} | {r['form']:<5} | {r['total_points']:<4} | {r['ict_index']:<5}")

if __name__ == "__main__":
    get_def_replacements()
