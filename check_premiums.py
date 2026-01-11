import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = requests.get(url).json()

names = ["Haaland", "Palmer", "Salah", "Isak", "Saka"]
for p in data['elements']:
    if any(n in p['web_name'] for n in names):
        print(f"{p['web_name']} ({p['now_cost']/10}): Form {p['form']} Pts {p['total_points']}")
