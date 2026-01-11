# FPL Master Strategy: The 4-4-2 "CBIT Monster" (GW21+)

**Manager:** Devendra Dhokare (ID: 17339)
**Strategy:** **The "Diamond Hands" Accumulation ➡️ 4-4-2 Power Shift**

## 🚨 MANDATORY AI RULES

_The AI MUST follow these rules before every recommendation:_

1.  **TEAM & RATING CHECK:** Check players current team from its id and then run a check on Fantasy hub AI team rating every time before researching and suggesting players and plans for GW transfers. Link: https://www.fantasyfootballhub.co.uk/ai-team-rating
2.  **ROSTER VERIFICATION:** Always check https://fantasy.premierleague.com/statistics for active 2025/26 players.
3.  **PRICE TRACKING:** Always check https://www.livefpl.net/prices for imminent price changes.
4.  **NEWS SOURCES:** Follow David Ornstein, Fabrizio Romano, and Ben Jacobs for January 2026 transfers.
5.  **AFCON 2026 AVAILABILITY:** Until Jan 18, 2026, ALWAYS verify AFCON status (e.g., Mbeumo returns GW23).
6.  **FIXTURE TRUTH:** ALWAYS verify the official 2025/26 fixture list.
7.  **SCORING 2025/26 (CBIT):** Incorporate the new "CBIT" metric. Defenders get +2 pts per 10 defensive actions.
8.  **DATA DEEP DIVE:** Check Home vs. Away splits and H2H history before transfers.
9.  **TACTICAL INTELLIGENCE:** Monitor manager changes (Man Utd/West Ham).
10. **PLAYER PERSISTENCE:** Remember: **Ollie Watkins** is the primary striker target (£9.0m), **Alexander Isak** is INJURED until March/April 2026, **Nicolas Jackson** is at Bayern Munich (Avoid).
11. **AUTOMATED DATA REFRESH:** Before every analysis, run `fetch_gw_stats.py --user dev` for the latest Gameweek. Update `Dev_Performance_Tracker.csv` and `Dev_Player_Performance.csv` to ensure "Weak Link" analysis is based on current xG/xA/xGC data.
12. **PRICE CHECK AUTOMATION:** Before recommending transfers, ALWAYS run `fetch_gw_stats.py` to get the latest `Cost` data in `[User]_Player_Performance.csv`. Use this actual data for budget calculations.

---

## 🏆 Current Squad State (GW21 Review)



**Fantasy Hub AI Rating:** **92%** (Verified Jan 8)

**GW21 Score:** 48 Pts (vs 3.56 xG) | **Team Value:** £102.4m



- **GK:** Pickford (3)

- **DEF:** Timber (6), Gabriel (6), Alderete (1), Rogers (3 - played DEF?)

- **MID:** Saka (3), Foden (2), Cunha (2), Rogers (3)

- **FWD:** Haaland (C) (6), DCL (8), Bowen (2)

- **Bench:** Dúbravka (3), Devenny (3), Van Hecke (3), Gudmundsson (0)



**Status:** A steady GW21 with 48 points. The xG of 3.56 suggests you were unlucky not to score more (Haaland 1.53 xG -> 6 pts).



### 📊 Squad Performance Matrix (GW19-GW21 Data)



_Analysis based on verified 'Dev_Player_Performance.csv' data._



| Player          | Mins (Last 3) | Avg Pts | Avg xG | Verdict        | Notes                                      |

|:----------------|:--------------|:--------|:-------|:---------------|:-------------------------------------------|

| **Haaland**     | 270           | 3.3     | 0.76   | 🥶 **Cold**    | Underlying stats (1.53 xG in GW21) suggest goals are coming. HOLD. |

| **DCL**         | 196           | 3.7     | 0.40   | 🦊 **Sneaky**  | 8 pts in GW21. Increasing value before sale. |

| **Bowen**       | 180           | 3.0     | 0.14   | ❌ **Sell**    | **PRIORITY OUT.** Poor xG, high price (£7.7m). |

| **Alderete**    | 172           | 1.0     | 0.09   | ⚠️ **Risk**    | Poor returns. Weak link in defence. |

| **Foden**       | 252           | 2.3     | 0.15   | 📉 **Drop**    | £8.8m is too much for 2 pts/game. Upgrade fund. |

| **Saka**        | 177           | 4.3     | 0.22   | 🛡️ **Anchor**  | Reliable. Keep. |

| **Rogers**      | 270           | 3.7     | 0.19   | 😐 **Hold**    | Consistent starter, decent enabler. |



---



## 🎯 The 4-4-2 Transition Plan (GW22-25)



**Objective:** Execute the "Power Shift" in GW23 to fix the Bowen/Foden issues and capitalize on the 3 accumulated Free Transfers.



### **Phase 1: The Patience (GW22)**



- **GW21:** ✅ **ROLLED** (Successfully banked FT).

- **GW22:** **ROLL TRANSFER** (Aiming for 3 FTs in GW23).

- **Strategy:** Hold the line. Do NOT sell Bowen yet unless price drops >£0.2m imminent. We need the 3 FTs to restructure without hits.



### **Phase 2: The GW23 "Power Shift" (3 FTs)**

- **OUT:** **Cunha (£8.2m)**, **Foden (£8.8m)**, **Bowen (£7.7m)**.
- **IN (Target):** **Enzo (CHE, £6.4m)**, **Palmer (CHE, £10.4m)**, **Thiago (BRE, £7.0m)**.
- **Immediate Move (GW22 - Optional):** **Cunha ➡️ Enzo**.
    - **Why?** Cunha faces MCI/ARS (Diff 4/5). Enzo faces BRE/CRY/WHU (Diff 3/3/2). Saves £1.8m.

### **Phase 3: The 4-4-2 Strike (GW24-25)**

- **GW24:** **SELL** DCL ➡️ **Ollie Watkins (AVL)** (£9.0m).
- **GW25:** **SELL** Timber ➡️ **Antonee Robinson** (FUL) or **James Tarkowski** (EVE).
- **Formation:** Final shift to **4-4-2**.

---

## 🔭 The "Diamond Hands" Watchlist (GW22-23)

_Tracking potential targets for the GW23 Power Shift._

| Player | Team | Price | Role | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Enzo** | CHE | £6.4m | **Cunha Rep** | 🔥 **BUY NOW** | 92 Pts. Amazing fixtures (BRE, CRY, WHU). Saves £1.8m. |
| **Thiago** | BRE | £7.0m | **Bowen Rep** | 🔥 **Top Pick** | Outscoring Bowen by 20pts. £0.7m cheaper. |
| **Raúl Jiménez** | FUL | £6.2m | **Budget FWD** | 💰 **Value** | Enables the Palmer upgrade. Good form (4.7). |
| **Cole Palmer** | CHE | £10.4m | **Essential** | ✅ **BUY GW23** | The Foden replacement. Non-negotiable. |
| **Lewis Hall** | NEW | £5.3m | **CBIT Gem** | ✅ **BUY GW23** | High xA potential. |
