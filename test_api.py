import requests
import json

def test_register():
    url = "http://localhost:8000/api/users/register"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure FastAPI is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_register() 