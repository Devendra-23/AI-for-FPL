import requests
import json

def check_player_and_sunderland():
    try:
        # Fetch Static Data
        static_data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
        teams = {t['id']: t['name'] for t in static_data['teams']}
        
        # Check Players
        target_players = ['Guéhi', 'Muñoz']
        for p_name in target_players:
            found = False
            for p in static_data['elements']:
                if p['web_name'] == p_name:
                    print(f"Player: {p_name} | Team: {teams[p['team']]} | Cost: {p['now_cost']/10}m | Status: {p['status']}")
                    found = True
                    break
            if not found:
                print(f"Player: {p_name} NOT FOUND")

        # Check Sunderland Home Record (Team ID 17)
        # We need to fetch fixtures and filter for Team 17 at home that are finished
        fixtures = requests.get('https://fantasy.premierleague.com/api/fixtures/').json()
        sun_home_games = [f for f in fixtures if f['team_h'] == 17 and f['finished'] == True]
        
        print("\nSunderland Home Record (2025/26):")
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        
        for f in sun_home_games:
            opponent = teams[f['team_a']]
            score_h = f['team_h_score']
            score_a = f['team_a_score']
            result = "D"
            if score_h > score_a:
                result = "W"
                wins += 1
            elif score_a > score_h:
                result = "L"
                losses += 1
            else:
                draws += 1
            
            goals_for += score_h
            goals_against += score_a
            
            print(f"vs {opponent}: {score_h}-{score_a} ({result})")
            
        print(f"\nSummary: W{wins}-D{draws}-L{losses}")
        print(f"Goals: {goals_for} Scored, {goals_against} Conceded")
        if wins + draws + losses > 0:
            print(f"Clean Sheets: {len([f for f in sun_home_games if f['team_a_score'] == 0])}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_player_and_sunderland()
