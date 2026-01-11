import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

# The user's list: Kelleher, Timber, Hall, Alderete, Gabriel, Dubravka, Gudmundsson, Wilson, Kroupi
targets = [
    ("Kelleher", "Kelleher"),
    ("Timber", "Timber"),
    ("Hall", "Hall"),
    ("Alderete", "Alderete"),
    ("Gabriel", "Gabriel"),
    ("Dubravka", "Dúbravka"),
    ("Gudmundsson", "Gudmundsson"),
    ("Wilson", "Wilson"),
    ("Kroupi", "Kroupi.Jr")
]

results = {}
for display_name, search_name in targets:
    for p in elements:
        if search_name.lower() in p['web_name'].lower():
             results[display_name] = p['now_cost'] / 10
             break

for k, v in results.items():
    print(f"{k}: £{v}m")

total = sum(results.values())
# Add one 4.0m fodder defender to reach 5 DEFs (assuming the 4 listed are starters/bench)
# Add 4.0 for the 5th DEF
total += 4.0 

print(f"\nSubtotal (9 players + 1 fodder DEF): £{total}m")
print(f"Remaining for 5 players (3 MIDs, 2 FWDs): £{100.3 - total:.1f}m")
