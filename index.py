import os
from dotenv import load_dotenv
import requests

# Load .env variables
load_dotenv()

# Access the token
API_TOKEN = os.getenv("CANVAS_API_TOKEN")
COURSE_ID = 422848
ASSIGNMENT_ID = 2054428

url = f"https://gatech.instructure.com/api/v1/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID}"
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    assignment = response.json()
    print("Assignment Name:", assignment["name"])
    print("Due Date:", assignment.get("due_at"))
    print("Points Possible:", assignment["points_possible"])
else:
    print("Error:", response.status_code)
