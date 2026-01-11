import requests

# 1. Fetch Data
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()

elements = {p['web_name']: p for p in data['elements']}
teams = {t['id']: t for t in data['teams']}

# Helper: Get Player Stats
def get_p(name):
    # Fuzzy match
    for n, p in elements.items():
        if name.lower() in n.lower():
            return p
    return None

# Helper: Calculate FDR for next 4 GWs (GW22-25)
gw_start = 22
gw_end = 25
team_fdr = {id: [] for id in teams.keys()}

for f in fixtures:
    if gw_start <= f['event'] <= gw_end:
        team_fdr[f['team_h']].append(f['team_h_difficulty'])
        team_fdr[f['team_a']].append(f['team_a_difficulty'])

avg_fdr = {}
for tid, diffs in team_fdr.items():
    avg_fdr[tid] = sum(diffs)/len(diffs) if diffs else 3.0

# xP Formula: Form * (1 + (3 - FDR)*0.1) * 4 games
# This simplifies: Better form + Easier fixtures = Higher Score
def calc_xp(player_name):
    p = get_p(player_name)
    if not p:
        return 0, 0
    
    tid = p['team']
    fdr = avg_fdr.get(tid, 3.0)
    form = float(p['form'])
    
    # Adjust form factor
    # If form is very low (<2), assume "base" potential of 2.0 (appearance pts)
    # If form is high, use it.
    base_proj = max(form, 2.0)
    
    # Fixture multiplier:
    # FDR 2 (Easy) -> 1.1x
    # FDR 3 (Avg) -> 1.0x
    # FDR 4 (Hard) -> 0.9x
    fdr_mult = 1 + (3 - fdr) * 0.1
    
    xp_per_game = base_proj * fdr_mult
    total_xp = xp_per_game * 4
    
    return total_xp, fdr

# Define Teams
team_wildcard = [
    "Kelleher", "Gabriel", "Collins", "Tarkowski", 
    "Saka", "Rice", "Rogers", "Wilson", "Garner", 
    "Haaland", "Thiago" # DCL is sub or rotation? Let's assume 3-5-2 or 3-4-3
]
# Let's start the best 11. DCL form is 6.8, Garner 6.5. 
# 3-4-3 is better: Saka, Rice, Rogers, Wilson (Garner bench) + Haaland, Thiago, DCL.
team_wildcard_11 = [
    "Kelleher", "Gabriel", "Collins", "Tarkowski",
    "Saka", "Rice", "Rogers", "Wilson",
    "Haaland", "Thiago", "Calvert-Lewin"
]

team_template_11 = [
    "Raya", "Guéhi", "Gabriel", "Van de Ven",
    "Semenyo", "Foden", "Rogers", "Rice", 
    "Haaland", "Thiago", "João Pedro"
]

print(f"{ 'PLAYER':<15} {'TEAM':<5} {'FORM':<5} {'FDR':<5} {'xP (4GW)':<10}")
print("-" * 50)

total_wc = 0
print("--- WILDCARD XI ---")
for name in team_wildcard_11:
    xp, fdr = calc_xp(name)
    p = get_p(name)
    print(f"{name:<15} {teams[p['team']]['short_name']:<5} {p['form']:<5} {fdr:.2f} {xp:.2f}")
    total_wc += xp

total_temp = 0
print("\n--- TEMPLATE XI ---")
for name in team_template_11:
    xp, fdr = calc_xp(name)
    p = get_p(name)
    print(f"{name:<15} {teams[p['team']]['short_name']:<5} {p['form']:<5} {fdr:.2f} {xp:.2f}")
    total_temp += xp

print("\n" + "="*40)
print(f"Wildcard Projected: {total_wc:.2f} pts")
print(f"Template Projected: {total_temp:.2f} pts")
print(f"DIFFERENCE: {total_wc - total_temp:.2f} pts")
