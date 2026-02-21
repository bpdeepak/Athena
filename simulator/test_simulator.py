import pprint
import httpx
import time

API_URL = "http://localhost:8001"

def test_api():
    print("Testing Mock Jira API...")
    
    # 1. Create User
    user_data = {
        "email": "test@athena.com",
        "name": "Jane Doe",
        "role": "PM"
    }
    r = httpx.post(f"{API_URL}/users", json=user_data)
    print("Create User:", r.status_code)
    user = r.json()
    
    # 2. Create Epic
    epic_data = {
        "id": "EPIC-100",
        "title": "Migrate to Cloud",
        "description": "Move all on-prem servers to AWS"
    }
    r = httpx.post(f"{API_URL}/epics", json=epic_data)
    print("Create Epic:", r.status_code)
    
    # 3. Create Story
    story_data = {
        "id": "STORY-101",
        "title": "Provision EC2 Instances",
        "epic_id": "EPIC-100",
        "assignee_id": user["id"],
        "priority": "HIGH"
    }
    r = httpx.post(f"{API_URL}/stories", json=story_data)
    print("Create Story:", r.status_code)
    
    # 4. Update Story
    r = httpx.put(f"{API_URL}/stories/STORY-101", json={"status": "IN_PROGRESS"})
    print("Update Story:", r.status_code)
    
    # 5. Get Stories
    r = httpx.get(f"{API_URL}/stories")
    print("Get Stories:", r.status_code)
    pprint.pprint(r.json())
    
if __name__ == "__main__":
    test_api()
