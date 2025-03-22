import requests
import concurrent.futures
import time
import logging
from tqdm import tqdm

def check_single_username(username, base_url, proxy=None, attempt=1, max_attempts=3):
    try:
        url = f"{base_url}{username}"
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, timeout=5, proxies=proxies)
        
        if response.status_code == 429:  # Too Many Requests
            if attempt >= max_attempts:
                logging.warning(f"Max attempts reached for {url}")
                return False
            delay = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s
            logging.warning(f"Rate limited at {url}, retrying in {delay}s")
            time.sleep(delay)
            return check_single_username(username, base_url, proxy, attempt + 1, max_attempts)
        
        return response.status_code == 200
    
    except requests.RequestException as e:
        logging.error(f"Error checking {url}: {str(e)}")
        return False

def check_usernames(username, sites, proxy=None):
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_site = {
            executor.submit(check_single_username, username, url, proxy): site 
            for site, url in sites.items()
        }
        
        # Progress bar
        with tqdm(total=len(sites), desc="Progress") as pbar:
            for future in concurrent.futures.as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    results[site] = future.result()
                except Exception as e:
                    results[site] = False
                    logging.error(f"Exception for {site}: {str(e)}")
                pbar.update(1)
    
    return results