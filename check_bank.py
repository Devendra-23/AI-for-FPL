import requests
import json

url = "https://fantasy.premierleague.com/api/entry/4669858/history/"
response = requests.get(url)
data = response.json()
current_gw = data['current'][-1]
print(f"GW: {current_gw['event']}")
print(f"Bank: {current_gw['bank']}")
print(f"Value: {current_gw['value']}")
print(f"Transfers: {current_gw['event_transfers']}")
print(f"Cost: {current_gw['event_transfers_cost']}")
