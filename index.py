import requests

# Replace this with your actual token
API_TOKEN = "2096~TnBTL7VnZX9AXDhVErnBATaVzZ67VxCxB78R6an6XVZFcnvCDhfM9mfcNVAc6xkm"
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
    print("Description:", assignment["description"])
else:
    print("Failed to fetch assignment. Status Code:", response.status_code)
    print(response.text)
