import requests
import os

PINTEREST_ACCESS_TOKEN = os.getenv("PROD_PINTEREST_ACCESS_TOKEN")
url = "https://api.pinterest.com/v5/boards"
headers = {"Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}"}
response = requests.get(url, headers=headers)
boards = response.json()["items"]
for board in boards:
    print(f"Board: {board['name']}, ID: {board['id']}")
