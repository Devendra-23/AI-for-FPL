import requests
import json
from collections import defaultdict

def analyze_fixtures():
    url = 'https://fantasy.premierleague.com/api/fixtures/'
    response = requests.get(url)
    fixtures = response.json()
    
    # Get team names
    bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    bootstrap_data = requests.get(bootstrap_url).json()
    teams = {t['id']: t['name'] for t in bootstrap_data['teams']}
    
    # Group fixtures by Event
    events = defaultdict(lambda: defaultdict(list))
    
    for f in fixtures:
        event = f.get('event')
        if event and event >= 25 and event <= 30: # Look ahead GW 25-30
            h_team = teams[f['team_h']]
            a_team = teams[f['team_a']]
            events[event][h_team].append(f"vs {a_team} (H)")
            events[event][a_team].append(f"vs {h_team} (A)")

    print("--- FIXTURE ANALYSIS (GW 25-30) ---")
    for event_id in sorted(events.keys()):
        print(f"\nGameweek {event_id}:")
        dgw_teams = []
        bgw_teams = []
        
        # Check for DGWs
        for team, matches in events[event_id].items():
            if len(matches) > 1:
                dgw_teams.append(f"{team}: {', '.join(matches)}")
        
        # Check for Blanks (teams with 0 matches)
        all_teams = set(teams.values())
        playing_teams = set(events[event_id].keys())
        bgw_teams = list(all_teams - playing_teams)
        
        if dgw_teams:
            print(f"  🚨 DOUBLE GAMEWEEK ALERT:")
            for t in dgw_teams:
                print(f"    - {t}")
        else:
            print(f"  No Doubles.")
            
        if bgw_teams:
            print(f"  ⚠️ BLANK GAMEWEEK ALERT:")
            print(f"    - {', '.join(sorted(bgw_teams))}")
        else:
            print(f"  No Blanks.")

if __name__ == "__main__":
    analyze_fixtures()
