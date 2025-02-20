import requests
import os

DATA_URL = "https://raw.githubusercontent.com/.../sf_crime.csv"
LOCAL_FILE = "data/sf_crime.csv"

def update_data():
    print("Fetching latest SF Crime data...")
    response = requests.get(DATA_URL, timeout=10)
    response.raise_for_status()
    
    os.makedirs("data", exist_ok=True)
    with open(LOCAL_FILE, "wb") as f:
        f.write(response.content)
    print("Data updated successfully!")

if __name__ == "__main__":
    update_data()
