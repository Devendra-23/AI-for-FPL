import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
elements = data['elements']

for p in elements:
    if "Cunha" in p['web_name']:
        print(f"{p['web_name']}: Type {p['element_type']} (3=MID, 4=FWD)")
