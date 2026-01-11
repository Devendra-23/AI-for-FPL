import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

print(f"{'NAME':<20} {'TEAM':<5} {'PRICE':<5} {'FORM':<5} {'PTS':<5}")
print("-" * 50)

for p in elements:
    if p['element_type'] == 3 and 5.5 <= p['now_cost']/10 <= 7.2:
        if p['status'] != 'u' and p['status'] != 'i':
             print(f"{p['web_name']:<20} {data['teams'][p['team']-1]['short_name']:<5} {p['now_cost']/10:<5} {p['form']:<5} {p['total_points']:<5}")

