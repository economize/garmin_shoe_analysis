import os
import json
from datetime import date, timedelta
from dotenv import load_dotenv
from garminconnect import Garmin
from garminconnect import (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

# --- 1. SETUP & AUTHENTICATION ---
def init_garmin_client():
    """
    Loads credentials from .env and logs into Garmin.
    Returns the authenticated client object.
    """
    # Load the hidden .env file
    load_dotenv()
    
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASS")

    # Safety Check: Did the .env load correctly?
    if not email or not password:
        print("❌ ERROR: Credentials not found.")
        print("   Please ensure your .env file exists and has GARMIN_EMAIL and GARMIN_PASS.")
        return None

    try:
        print(f"🔐 Authenticating as {email}...")
        client = Garmin(email, password)
        client.login()
        print("✅ Login successful!")
        return client

    except (GarminConnectAuthenticationError):
        print("❌ ERROR: Authentication failed. Check your password in .env.")
        return None
    except (GarminConnectTooManyRequestsError):
        print("❌ ERROR: Too many requests. Garmin has temporarily blocked this IP. Try again in an hour.")
        return None
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred: {e}")
        return None

# --- 2. DATA FETCHING ---
def fetch_recent_activities(client, days=30):
    """
    Fetches activity data (runs, etc.) for the last 'days'.
    """
    today = date.today()
    start_date = today - timedelta(days=days)
    
    print(f"📡 Fetching data from {start_date} to {today}...")

    try:
        # Fetch activities (This contains your Heart Rate, Pace, and Training Load data)
        activities = client.get_activities_by_date(
            start_date.isoformat(), 
            today.isoformat()
        )
        print(f"✅ Successfully fetched {len(activities)} activities.")
        return activities
        
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
        return []

# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
    # A. Login
    garmin_client = init_garmin_client()

    # B. If login worked, fetch data
    if garmin_client:
        recent_data = fetch_recent_activities(garmin_client, days=30)
        
        # C. Save raw data to inspect (Essential for Data Science steps later)
        if recent_data:
            output_file = "garmin_raw_data.json"
            with open(output_file, "w") as f:
                json.dump(recent_data, f, indent=4)
            print(f"💾 Data saved to '{output_file}'. You can now open this file to inspect the JSON structure.")