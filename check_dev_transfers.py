import requests

url = "https://fantasy.premierleague.com/api/entry/17339/history/"
data = requests.get(url).json()
current = data['current'][-1] # This should be GW21

# Note: In 2025/26, FPL allows accumulating up to 5 Free Transfers.
# We need to see how many were available in GW21 and if any were used.

print(f"Manager: Dev (17339)")
print(f"Latest GW in History: {current['event']}")
print(f"Bank: {current['bank']}")
print(f"Transfers made in latest GW: {current['event_transfers']}")

# To know EXACTLY how many FTs are currently available, we check the entry data
entry_url = "https://fantasy.premierleague.com/api/entry/17339/"
entry_data = requests.get(entry_url).json()
# This doesn't explicitly show "Available FTs" but we can infer from logs or previous turns.
# Based on Dev.md: "GW21: ROLLED (Banked FT)".
