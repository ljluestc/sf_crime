import requests
import os
import pandas as pd

# SF Open Crime API endpoint (Police Department Incident Reports)
API_URL = "https://data.sfgov.org/resource/cuks-n6tp.json?$limit=50000"
LOCAL_FILE = "data/sf_crime.csv"

def fetch_and_save_data():
    print("Fetching latest SF Crime data...")
    try:
        # Fetch data from the API
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Ensure required columns are present and rename if necessary
        df = df.rename(columns={'x': 'X', 'y': 'Y', 'category': 'Category'})
        if 'X' not in df.columns or 'Y' not in df.columns or 'Category' not in df.columns:
            print("Warning: Required columns missing from API data.")

        # Save to local file
        os.makedirs("data", exist_ok=True)
        df.to_csv(LOCAL_FILE, index=False)
        print("Data updated successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_data()