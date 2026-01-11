import json
import csv
import urllib.request
import ssl
import sys

# Configuration
USER_FILE = 'Dev_Player_Performance.csv'
JSON_FILE = 'fpl_data.json'
GW = 22

def fetch_json(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_player_stats_from_csv():
    stats = {}
    try:
        with open(USER_FILE, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            # Find latest available data (GW21)
            # We want to know if they are playing (Mins > 0) and their average points
            
            for row in reader:
                if not row: continue
                name = row[0]
                
                # Simple Logic: Check last 3 GWs (19, 20, 21)
                # We'll just take the latest "Form" from fpl_data if possible, 
                # but let's use the CSV to confirm they are actually in the team.
                stats[name] = {
                    'in_team': True
                }
    except FileNotFoundError:
        pass
    return stats

def main():
    print(f"🔮 PREDICTING GAMEWEEK {GW} SCORES")
    print("-" * 60)

    # 1. Load Static Data
    try:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
        elements = data['elements']
        teams = data['teams']
    except Exception as e:
        print(f"Error loading {JSON_FILE}: {e}")
        return

    # 2. Fetch Fixtures
    fixtures = fetch_json(f"https://fantasy.premierleague.com/api/fixtures/?event={GW}")
    if not fixtures:
        print("Could not fetch fixtures.")
        return

    # Map Team ID to Fixture Difficulty
    # simplified: {team_id: {opponent_id, difficulty, is_home}}
    team_fixtures = {}
    for f in fixtures:
        h = f['team_h']
        a = f['team_a']
        h_diff = f['team_h_difficulty']
        a_diff = f['team_a_difficulty']
        
        team_fixtures[h] = {'opp': a, 'diff': h_diff, 'is_home': True}
        team_fixtures[a] = {'opp': h, 'diff': a_diff, 'is_home': False}

    # 3. Predict Scores
    # Algorithm: (Form * 0.5) + (FixtureRating * 2) + (HomeAdvantage * 0.5)
    # FixtureRating: 5 - Difficulty (Easier is better)
    
    predictions = []
    
    # Get user's players from CSV
    user_players = get_player_stats_from_csv()
    
    for p in elements:
        # Match by name (fuzzy or direct)
        # In CSV names are "Haaland", "Saka". In JSON "Erling Haaland", "Bukayo Saka".
        # We need to map them.
        
        found = False
        csv_name = ""
        for u_name in user_players:
            if u_name in p['web_name'] or p['web_name'] in u_name:
                found = True
                csv_name = u_name
                break
        
        if not found:
            continue

        team_id = p['team']
        if team_id not in team_fixtures:
            # Blank Gameweek?
            predicted_pts = 0
            fixture_note = "BLANK"
        else:
            fix = team_fixtures[team_id]
            diff = fix['diff']
            is_home = fix['is_home']
            
            # Base Projection
            form = float(p['form'])
            fixture_score = (6 - diff) # 1(hard)=5pts, 5(hard)=1pt. Wait. 1 is easy.
            # Difficulty: 1 (Easy) -> 5 (Hard)
            # We want: 1 -> +2 pts, 5 -> -1 pt?
            # Let's do: Base 2 pts + (5 - diff) * 0.5 + (Form * 0.4)
            
            base = 2.0 # Appearance
            fix_bonus = (5 - diff) * 0.6
            form_bonus = form * 0.4
            home_bonus = 0.5 if is_home else 0.0
            
            # Position modifiers
            pos_bonus = 0
            if p['element_type'] == 1: # GKP
                pos_bonus = 0.5 # Save points potential
            if p['element_type'] == 2: # DEF
                pos_bonus = 0.5 if diff <= 2 else 0 # CS potential
            if p['element_type'] >= 3: # ATT
                pos_bonus = 0.5 if diff <= 3 else 0 # Goal potential
                
            predicted_pts = base + fix_bonus + form_bonus + home_bonus + pos_bonus
            
            opp_name = next((t['short_name'] for t in teams if t['id'] == fix['opp']), "?")
            venue = "(H)" if is_home else "(A)"
            fixture_note = f"vs {opp_name} {venue}"

        predictions.append({
            'name': p['web_name'],
            'pos': p['element_type'],
            'pts': round(predicted_pts, 1),
            'fix': fixture_note,
            'cost': p['now_cost'] / 10
        })

    # 4. Sort and Display
    # Sort by Points Descending
    predictions.sort(key=lambda x: x['pts'], reverse=True)
    
    print(f"{'Name':<15} | {'Pos':<3} | {'Pred':<5} | {'Fixture':<10}")
    print("-" * 50)
    
    # Separate into Position Groups for display
    # We need to build a valid formation (1 GK, 3-5 DEF, 2-5 MID, 1-3 FWD)
    # The user wants "Order of Squad".
    
    # 1. Select GK (Top projected)
    gkps = [p for p in predictions if p['pos'] == 1]
    outfield = [p for p in predictions if p['pos'] != 1]
    
    starters = []
    bench = []
    
    if gkps:
        starters.append(gkps[0])
        bench.extend(gkps[1:])
    
    # 2. Select Outfield (Top 10)
    # But must respect formation rules. 
    # Min 3 Defenders, Min 1 FWD?
    # Let's just pick top 10 outfielders first, then check constraints.
    
    # Actually, easier: Pick top players, ensure min 3 DEF, min 2 MID, min 1 FWD.
    # Current squad has 15 players. 2 GK (handled). 13 Outfield. Pick 10.
    
    defs = sorted([p for p in predictions if p['pos'] == 2], key=lambda x: x['pts'], reverse=True)
    mids = sorted([p for p in predictions if p['pos'] == 3], key=lambda x: x['pts'], reverse=True)
    fwds = sorted([p for p in predictions if p['pos'] == 4], key=lambda x: x['pts'], reverse=True)
    
    # Mandatory slots
    selected_defs = defs[:3]
    selected_mids = mids[:2]
    selected_fwds = fwds[:1]
    
    remaining_pool = defs[3:] + mids[2:] + fwds[1:]
    remaining_pool.sort(key=lambda x: x['pts'], reverse=True)
    
    # Fill last 4 slots
    flex_spots = remaining_pool[:4]
    bench_spots = remaining_pool[4:]
    
    starting_xi = selected_defs + selected_mids + selected_fwds + flex_spots
    
    # Sort Starting XI by Position (GK-DEF-MID-FWD)
    starting_xi.sort(key=lambda x: x['pos'])
    
    # Display Starters
    print("\n🟢 STARTING XI")
    print(f"{starters[0]['name']:<15} | GKP | {starters[0]['pts']:<5} | {starters[0]['fix']}")
    for p in starting_xi:
        pos_str = {2:'DEF', 3:'MID', 4:'FWD'}[p['pos']]
        print(f"{p['name']:<15} | {pos_str} | {p['pts']:<5} | {p['fix']}")
        
    # Display Bench
    print("\n🔴 BENCH (Order)")
    for p in bench_spots:
        pos_str = {2:'DEF', 3:'MID', 4:'FWD'}[p['pos']]
        print(f"{p['name']:<15} | {pos_str} | {p['pts']:<5} | {p['fix']}")
    
    for p in bench: # GKs
         print(f"{p['name']:<15} | GKP | {p['pts']:<5} | {p['fix']}")
         
    # Captaincy
    all_starters = starters + starting_xi
    captain = max(all_starters, key=lambda x: x['pts'])
    vice = sorted(all_starters, key=lambda x: x['pts'], reverse=True)[1]
    
    print(f"\n©️ CAPTAIN: {captain['name']} ({captain['pts']})")
    print(f"🔄 VICE:    {vice['name']} ({vice['pts']})")

if __name__ == "__main__":
    main()
