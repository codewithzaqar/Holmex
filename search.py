import requests
import concurrent.futures
import time
import logging

def check_single_username(username, base_url):
    try:
        url = f"{base_url}{username}"
        response = requests.get(url, timeout=5)

        if response.status_code == 429:  # Too Many Requests
            logging.warning(f"Rate limited at {url}")
            time.sleep(2)  # Basic rate limit handling
            return check_single_username(username, base_url)  # Retry once

        return response.status_code == 200
    
    except requests.RequestException as e:
        logging.error(f"Error checking {url}: {str(e)}")
        return False

def check_usernames(username, sites):
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_site = {
            executor.submit(check_single_username, username, url): site 
            for site, url in sites.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            try:
                results[site] = future.result()
            except Exception as e:
                results[site] = False
                logging.error(f"Exception for {site}: {str(e)}")
    
    return results