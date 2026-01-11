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
    
    # 1. Find Bowen
    bowen = next((p for p in elements if "Bowen" in p['web_name']), None)
    if not bowen:
        print("Error: Bowen not found in database.")
        return

    print(f"TARGET: {bowen['web_name']}")
    print(f"ID: {bowen['id']}")
    print(f"Position ID: {bowen['element_type']} (3=MID, 4=FWD)")
    print(f"Current Price: £{bowen['now_cost'] / 10}m")
    print(f"Form: {bowen['form']}")
    print(f"Total Points: {bowen['total_points']}")
    print("-" * 30)

    # 2. Find Replacements
    # We want players of same position, price <= (Bowen + 0.5m buffer just in case), sorted by Form/ICT
    
    replacements = []
    
    for p in elements:
        # Same position
        if p['element_type'] != bowen['element_type']:
            continue
            
        # Ignore Bowen himself
        if p['id'] == bowen['id']:
            continue
            
        # Price constraint (let's show options up to +1.0m just in case user has bank, but focus lower)
        # Bowen is ~7.7. Let's look up to 9.0 and down to 5.0
        price = p['now_cost'] / 10
        if price > (bowen['now_cost'] / 10 + 1.5): # Cap slightly higher
            continue

        # Filter by form or points to remove dead wood
        if float(p['form']) < 3.0 and p['total_points'] < 50:
            continue
            
        replacements.append(p)

    # Sort by Form descending
    replacements.sort(key=lambda x: float(x['form']), reverse=True)

    print(f"{'Name':<20} | {'Team':<4} | {'Price':<6} | {'Form':<5} | {'Pts':<4} | {'ICT':<5}")
    print("-" * 65)
    
    for r in replacements[:15]: # Top 15 options
        # Map Team ID (simplified, usually 1-20)
        print(f"{r['web_name']:<20} | {r['team']:<4} | £{r['now_cost']/10:<5} | {r['form']:<5} | {r['total_points']:<4} | {r['ict_index']:<5}")

if __name__ == "__main__":
    get_replacements()
