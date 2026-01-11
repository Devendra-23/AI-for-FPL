import requests

# Fetch Data
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()

elements = {p['web_name']: p for p in data['elements']}

def get_p(name):
    # Precise match first, then fuzzy
    for n, p in elements.items():
        if name == n: return p
    for n, p in elements.items():
        if name in n: return p
    return None

# FDR Setup
gw_start = 22
gw_end = 25
team_fdr = {t['id']: [] for t in data['teams']}
for f in fixtures:
    if gw_start <= f['event'] <= gw_end:
        team_fdr[f['team_h']].append(f['team_h_difficulty'])
        team_fdr[f['team_a']].append(f['team_a_difficulty'])
avg_fdr = {tid: sum(d)/len(d) if d else 3.0 for tid, d in team_fdr.items()}

def calc_xp(name):
    p = get_p(name)
    if not p: return 0, 0, 0
    tid = p['team']
    fdr = avg_fdr.get(tid, 3.0)
    form = float(p['form'])
    # xP Logic
    base = max(form, 2.0)
    mult = 1 + (3 - fdr) * 0.1
    return base * mult * 4, form, fdr

comparisons = [
    ("Tavernier", "Wilson"), # BOU vs FUL
    ("Chalobah", "Tarkowski"), # CHE vs EVE
    ("Gusto", "Tarkowski"), # CHE vs EVE
    ("João Pedro", "Calvert-Lewin"), # CHE vs LEE
    ("Palmer", "Saka") # CHE vs ARS
]

print(f"{'PLAYER':<15} {'FORM':<5} {'FDR':<5} {'xP (4GW)':<10}")
print("-" * 40)

for p1, p2 in comparisons:
    xp1, f1, fdr1 = calc_xp(p1)
    xp2, f2, fdr2 = calc_xp(p2)
    print(f"{p1:<15} {f1:<5} {fdr1:.2f} {xp1:.2f}")
    print(f"{p2:<15} {f2:<5} {fdr2:.2f} {xp2:.2f}")
    print(f"Winner: {p1 if xp1 > xp2 else p2} (+{abs(xp1-xp2):.2f})")
    print("-" * 40)
