import requests

url = "http://127.0.0.1:5000/api/execute-trade"
payload = {
    "symbol": "AAPL",          # You can change to any stock supported by Alpaca
    "quantity": 1,
    "duration": "day"          # Placeholder; you can enhance this logic later
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())
