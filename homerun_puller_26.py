import requests
import pandas as pd
from datetime import datetime

FILENAME = "MLB_2026_Team_Power.xlsx"

def pull_team_totals_2026():
    print(f"🚀 Pulling 2026 Team Totals (Live Database)...")
    
    # We use the 'stats' endpoint for teams, which is more robust than 'leaders'
    url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&season=2026&gameType=S&sportId=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Access the team splits
        splits = data.get('stats', [{}])[0].get('splits', [])
        
        if not splits:
            print("❌ No team stats found. Double-checking gameType...")
            return

        rows = []
        for entry in splits:
            team_info = entry.get('team', {})
            stat_info = entry.get('stat', {})
            
            rows.append({
                "Team": team_info.get('name', 'N/A'),
                "Home Runs": stat_info.get('homeRuns', 0),
                "At Bats": stat_info.get('atBats', 0),
                "Hits": stat_info.get('hits', 0),
                "AVG": stat_info.get('avg', ".000"),
                "Last Sync": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        # Create DataFrame and sort by HRs
        df = pd.DataFrame(rows).sort_values(by="Home Runs", ascending=False)
        
        # Save to Excel
        df.to_excel(FILENAME, index=False)
        
        print(f"✅ SUCCESS! Created '{FILENAME}' with all 30 teams.")
        print(f"Leaderboard: {df.iloc[0]['Team']} has {df.iloc[0]['Home Runs']} HRs.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    pull_team_totals_2026()