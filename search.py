import requests

def check_username(username, base_url):
    try:
        url = f"{base_url}{username}"
        response = requests.get(url, timeout=5)
        
        # Basic status check (200 means page exists)
        if response.status_code == 200:
            return True
        return False
    
    except requests.RequestException:
        return False