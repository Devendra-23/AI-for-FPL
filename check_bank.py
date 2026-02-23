import requests
import json
import argparse

USERS = {
    'dev': 17339,
    'harriet': 2610341,
    'chris': 4669858,
    'adam': 7456922,
    'tommy': 348422,
    'ollie': 1501765
}

parser = argparse.ArgumentParser(description='Check FPL Bank Balance')
parser.add_argument('--user', type=str, default='dev', choices=list(USERS.keys()), help='Manager to check (dev, harriet, chris, etc.)')
args = parser.parse_args()

user_id = USERS[args.user]
url = f"https://fantasy.premierleague.com/api/entry/{user_id}/history/"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if 'current' in data and len(data['current']) > 0:
        current_gw = data['current'][-1]
        bank_value = current_gw['bank'] / 10.0
        team_value = current_gw['value'] / 10.0
        
        print(f"Manager: {args.user.upper()} (ID: {user_id})")
        print(f"GW: {current_gw['event']}")
        print(f"Bank: £{bank_value}m")
        print(f"Team Value: £{team_value}m")
        print(f"Transfers Made: {current_gw['event_transfers']}")
        print(f"Transfer Cost: {current_gw['event_transfers_cost']}")
    else:
        print("No gameweek history found.")

except Exception as e:
    print(f"Error fetching bank data: {e}")
