import requests
import os
import json

API_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/jardins-partages/records"

def fetch_data(limit=100, offset=0):
    """Fetch data from OpenData Paris API"""
    params = {"limit": limit, "offset": offset}
    print(f"[DEBUG] Fetching data from: {API_URL} with params: {params}")
    
    try:
        resp = requests.get(API_URL, params=params, timeout=30)
        print(f"[DEBUG] Status: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"[ERROR] API returned status {resp.status_code}")
            return []
        
        data = resp.json()
     
        records = data.get("results", [])
        print(f"[INFO] Batch fetched: {len(records)} records (offset={offset})")
        
        # Save for debug
        os.makedirs("data", exist_ok=True)
        with open(f"data/debug_{offset}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return records
        
    except requests.Timeout:
        print(f"[ERROR] Timeout after 30s")
        return []
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return []