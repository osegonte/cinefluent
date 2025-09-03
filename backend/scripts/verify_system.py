#!/usr/bin/env python3
"""Quick system verification after cleanup"""

import requests

def verify_system():
    print("🔍 Verifying Cinefluent System...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Health check
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Server health: OK")
        else:
            print("❌ Server health failed")
            return False
            
        # Check movies
        response = requests.get(f"{base_url}/api/v1/movies/")
        if response.status_code == 200:
            movies = response.json()
            print(f"✅ Movies API: {len(movies)} movies found")
        else:
            print("❌ Movies API failed")
            return False
            
        # Quick user test
        login_data = {"username": "demouser", "password": "password123"}
        response = requests.post(f"{base_url}/api/v1/users/login", json=login_data)
        if response.status_code == 200:
            print("✅ User system: Login working")
        else:
            print("❌ User system failed")
            return False
            
        print("\n🎉 System verification complete - All core functions working!")
        return True
        
    except requests.exceptions.RequestException:
        print("❌ Server not running. Start with: uv run uvicorn app.main:app --reload")
        return False

if __name__ == "__main__":
    verify_system()