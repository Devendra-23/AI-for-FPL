import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

targets = ["Kelleher", "Timber", "Lewis Hall", "Alderete", "Gabriel", "Dubravka", "Gudmundsson", "Harry Wilson", "Junior Kroupi"]
fixed_costs = {}

for p in elements:
    name = p['web_name']
    for t in targets:
        if t.lower() in name.lower():
            fixed_costs[t] = p['now_cost'] / 10

# Print results
for name, cost in fixed_costs.items():
    print(f"{name}: £{cost}m")

# Sum fixed
total_fixed = sum(fixed_costs.values())
print(f"\nTotal Fixed Cost: £{total_fixed}m")
