import os
import json
import requests

token = os.getenv('ANOVA_TOKEN')
# Step 1: Load JSON from file
file = 'c:\\anovaFTP\\ftp\\data\\anova3.json'
success = True
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {token}'
}


try:
    with open(file, 'r') as f:
        batch_requests = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON error: {e}")
    success = False

if success:
    for item in batch_requests:
        url = item['url']
        data = item['data']

        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"POST to {url} => {response.status_code}")
            print(response.text[:300])  # Print first 300 chars of response for brevity
            with open("log.txt", "a") as log:
                log.write(f"{url} => {response.status_code}\n{response.text}\n\n")

        except Exception as e:
            print(f"Error posting to {url}: {e}")
            with open("log.txt", "a") as log:
                log.write(f"{url} ERROR => {str(e)}\n\n")

