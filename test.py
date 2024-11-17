from datetime import datetime
import httpx

def calculate(latitude,longitude, fromdate, to):
    host = "https://ei.palmetto.com/api/v0/"

    with httpx.Client() as handler:
        resp = handler.get(url=host+"health")
        print(resp.text)
    
        payload = {
            "location": {
              "latitude": 37.7749,
              "longitude": -122.4194
            },
              "parameters": {
              "from_datetime": "2019-01-01T00:00:00",
              "to_datetime": "2020-01-01T00:00:00",
            }
          }

        headers = {
            "accept" : "application/json",
            "content-type": "application/json",
            "X-API-Key": "WKGlTTo3KbjUZDmbatspnyMdnYTtunteJxbdY8c6ScE"
        }

        resp = handler.post(url=host+"bem/calculate", json=payload, headers=headers)

        print(resp.status_code)

calculate(10,120,"2024-11-15T23:43:30", "2024-11-16T23:43:30")
