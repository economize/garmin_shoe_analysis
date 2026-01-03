import duckdb
import pandas as pd
import json

# 1. Load the raw data fetched by fetch_data.py
try:
    with open('garmin_raw_data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: garmin_raw_data.json not found. Run fetch_data.py first.")
    exit()

# 2. Normalize and Prep Data
df = pd.json_normalize(data)

# Detect the best "Load" metric available
if 'trainingStressScore' in df.columns:
    df['load'] = df['trainingStressScore'].fillna(0)
    load_source = "Garmin TSS"
else:
    # Fallback: TRIMP proxy (Duration_mins * AvgHR)
    df['load'] = (df['duration'] / 60) * df['averageHR']
    load_source = "Calculated TRIMP"

df['date'] = pd.to_datetime(df['startTimeLocal']).dt.date
df = df.sort_values('date')

# 3. The DuckDB Analysis (Window Functions)
query = """
WITH daily_load AS (
    SELECT 
        date, 
        SUM(load) as daily_load 
    FROM df 
    GROUP BY date
),
rolling_stats AS (
    SELECT 
        date,
        daily_load,
        -- Acute (7-day avg)
        AVG(daily_load) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as acute,
        -- Chronic (28-day avg)
        AVG(daily_load) OVER (ORDER BY date ROWS BETWEEN 27 PRECEDING AND CURRENT ROW) as chronic
    FROM daily_load
)
SELECT 
    *,
    ROUND(acute / NULLIF(chronic, 0), 2) as acwr
FROM rolling_stats
ORDER BY date DESC
LIMIT 1
"""

# Run Query
result = duckdb.query(query).to_df()
latest = result.iloc[0]

# 4. Save Real Metrics for the Coach
real_metrics = {
    "acwr": float(latest['acwr']),
    "acute_load": float(latest['acute']),
    "chronic_load": float(latest['chronic']),
    "date": str(latest['date'])
}

# Save to a generic file the Coach can read
with open('latest_physio.json', 'w') as f:
    json.dump(real_metrics, f)

# 5. Report to User
print(f"✅ ANALYSIS COMPLETE ({load_source})")
print(f"📅 Date: {latest['date']}")
print(f"📊 ACWR: {latest['acwr']} (Acute: {latest['acute']:.0f} / Chronic: {latest['chronic']:.0f})")

if latest['acwr'] > 1.3:
    print("🚨 STATUS: HIGH RISK (Groin Guard Active)")
elif latest['acwr'] > 1.1:
    print("⚠️ STATUS: ELEVATED RISK")
else:
    print("🟢 STATUS: GREEN LIGHT")