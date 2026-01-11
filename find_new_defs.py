import requests

# Fetch Data
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']
teams = {t['id']: t['short_name'] for t in data['teams']}

# Filter Defenders
defenders = []
for p in elements:
    if p['element_type'] == 2 and p['status'] != 'u':
        defenders.append({
            'name': p['web_name'],
            'team': teams[p['team']],
            'price': p['now_cost'] / 10,
            'form': float(p['form']),
            'points': p['total_points'],
            'selected': float(p['selected_by_percent']),
            'ict': float(p['ict_index'])
        })

# Sort by Form
defenders.sort(key=lambda x: x['form'], reverse=True)

print(f"{ 'NAME':<20} {'TEAM':<5} {'PRICE':<5} {'FORM':<5} {'PTS':<5} {'SEL%':<5} {'ICT':<5}")
print("-" * 65)

# Top 20 Defenders by Form
for d in defenders[:20]:
    print(f"{d['name']:<20} {d['team']:<5} {d['price']:<5} {d['form']:<5} {d['points']:<5} {d['selected']:<5} {d['ict']:<5}")

print("\n--- SPECIFIC TARGETS (LIV, ARS, MCI, TOT) ---")
targets = ["Saliba", "White", "Timber", "Virgil", "Konaté", "Alexander-Arnold", "Gvardiol", "Porro", "Ait-Nouri", "Muñoz"]
for d in defenders:
    if any(t in d['name'] for t in targets):
         print(f"{d['name']:<20} {d['team']:<5} {d['price']:<5} {d['form']:<5} {d['points']:<5} {d['selected']:<5} {d['ict']:<5}")
