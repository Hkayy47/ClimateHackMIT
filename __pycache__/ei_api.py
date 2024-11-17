# ei_api.py
import requests
from config import EI_API_KEY  # Add your API key to config.py

BASE_URL = "https://api.ei.com/v1"  # Replace with actual base URL

headers = {
    "Authorization": f"Bearer {EI_API_KEY}",
    "Content-Type": "application/json"
}

def get_energy_calculation(latitude, longitude, start_date, end_date):
    payload = {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "parameters": {
            "from_datetime": start_date,
            "to_datetime": end_date,
            "group_by": "month"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/calculate", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"EI API request failed: {str(e)}")
