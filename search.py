import requests
import concurrent.futures

def check_single_username(username, base_url):
    try:
        url = f"{base_url}{username}"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_usernames(username, sites):
    results = {}
    
    # Use ThreadPoolExecutor for concurrent checking
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the checks
        future_to_site = {
            executor.submit(check_single_username, username, url): site 
            for site, url in sites.items()
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            try:
                result = future.result()
                results[site] = result
            except Exception as e:
                results[site] = False
    
    return results