import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

names = ["Palmer", "Saka", "Haaland", "Tavernier"]
total = 0
for n in names:
    for p in elements:
        if n.lower() in p['web_name'].lower():
            print(f"{p['web_name']}: £{p['now_cost']/10}m")
            total += p['now_cost']/10
            break

print(f"\nTotal for 4 players: £{total:.1f}m")
print(f"Remaining from £52.5m: £{52.5 - total:.1f}m")

