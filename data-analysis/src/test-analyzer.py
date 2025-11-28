import os 
import requests

with open("example.com-test-html", "r") as f:
    html_content = f.read()

API_URL = "http://localhost:8000/analyze"
API_KEY = "this-is-my-super-secure-api-key"

headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
}

payload = {
    "content": html_content
}
response = requests.post(API_URL, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())

