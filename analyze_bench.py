import requests

def analyze_bench_dilemma():
    # Load Data
    fixtures = requests.get('https://fantasy.premierleague.com/api/fixtures/').json()
    static = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
    teams = {t['id']: t['name'] for t in static['teams']}
    
    # Team IDs
    liv_id = [t['id'] for t in static['teams'] if t['name'] == 'Liverpool'][0]
    sun_id = [t['id'] for t in static['teams'] if t['name'] == 'Sunderland'][0]
    che_id = [t['id'] for t in static['teams'] if t['name'] == 'Chelsea'][0]
    lee_id = [t['id'] for t in static['teams'] if t['name'] == 'Leeds'][0]
    
    # Analyze Liverpool Recent Form
    print("Liverpool Last 5 Games:")
    liv_games = [f for f in fixtures if (f['team_h'] == liv_id or f['team_a'] == liv_id) and f['finished']][-5:]
    for f in liv_games:
        is_home = f['team_h'] == liv_id
        opponent = teams[f['team_a']] if is_home else teams[f['team_h']]
        score = f"{f['team_h_score']}-{f['team_a_score']}"
        loc = "(H)" if is_home else "(A)"
        print(f"  {score} vs {opponent} {loc}")

    # Analyze Chelsea Recent Form
    print("\nChelsea Last 5 Games:")
    che_games = [f for f in fixtures if (f['team_h'] == che_id or f['team_a'] == che_id) and f['finished']][-5:]
    for f in che_games:
        is_home = f['team_h'] == che_id
        opponent = teams[f['team_a']] if is_home else teams[f['team_h']]
        score = f"{f['team_h_score']}-{f['team_a_score']}"
        loc = "(H)" if is_home else "(A)"
        print(f"  {score} vs {opponent} {loc}")

if __name__ == "__main__":
    analyze_bench_dilemma()
