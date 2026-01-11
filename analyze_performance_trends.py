import csv
import sys

def analyze_performance():
    tracker_file = 'Dev_Performance_Tracker.csv'
    player_file = 'Dev_Player_Performance.csv'
    
    print("ANALYZING RECENT PERFORMANCE (GW19-21)...")
    print("-" * 50)
    
    # 1. Team Level Trends
    try:
        with open(tracker_file, 'r') as f:
            reader = list(csv.reader(f))
            header = reader[0]
            # Get last 3 rows
            recent_rows = reader[-3:]
            
            pts_idx = header.index("Gameweek Points")
            xg_idx = header.index("xG")
            
            print(f"{'GW':<5} | {'Pts':<5} | {'xG':<5} | {'Status'}")
            for row in recent_rows:
                gw = row[0]
                pts = row[pts_idx]
                xg = row[xg_idx]
                
                status = "OK"
                if float(pts) < 40: status = "LOW"
                if float(xg) < 2.0: status = "LOW xG"
                
                print(f"{gw:<5} | {pts:<5} | {xg:<5} | {status}")
                
    except Exception as e:
        print(f"Error reading tracker: {e}")

    print("-" * 50)
    print("UNDERPERFORMING PLAYERS (Last 3 GW Average < 3.0 pts)")
    print(f"{'Name':<20} | {'Avg Pts':<8} | {'Avg xG':<8} | {'Mins (Last 3)'}")
    
    # 2. Player Level Analysis
    try:
        with open(player_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Identify columns for last 3 GWs (19, 20, 21)
            # We look for columns like GW19_Pts, GW19_xG, GW19_Min
            
            target_gws = [19, 20, 21]
            player_data = {}
            
            for row in reader:
                name = row[0]
                total_pts = 0
                total_xg = 0.0
                total_mins = 0
                count = 0
                
                for gw in target_gws:
                    pts_col = f"GW{gw}_Pts"
                    xg_col = f"GW{gw}_xG"
                    min_col = f"GW{gw}_Min"
                    
                    try:
                        p_idx = header.index(pts_col)
                        x_idx = header.index(xg_col)
                        m_idx = header.index(min_col)
                        
                        if len(row) > p_idx and row[p_idx] not in ['-', '']:
                            total_pts += int(row[p_idx])
                            total_xg += float(row[x_idx])
                            total_mins += int(row[m_idx])
                            count += 1
                    except ValueError:
                        pass
                
                if count > 0:
                    avg_pts = total_pts / count
                    avg_xg = total_xg / count
                    
                    # Flag underperformers: Avg Pts < 3.5 OR (Low mins < 120 total over 3 GWs)
                    if avg_pts < 3.5 or total_mins < 120:
                         print(f"{name:<20} | {avg_pts:<8.1f} | {avg_xg:<8.2f} | {total_mins}")

    except Exception as e:
        print(f"Error reading players: {e}")

if __name__ == "__main__":
    analyze_performance()
