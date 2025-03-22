import requests
import concurrent.futures
import time
import logging
import random
from tqdm import tqdm

def check_single_username(username, site_info, proxies, config, attempt=1):
    base_url = site_info['url']
    success_codes = site_info.get('success_codes', [200])
    error_string = site_info.get('error_string')
    
    try:
        url = f"{base_url}{username}"
        proxy = random.choice(proxies) if proxies else None
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        
        response = requests.get(url, timeout=config['timeout'], proxies=proxies_dict)
        
        if response.status_code == 429:
            if attempt >= config['max_attempts']:
                logging.warning(f"Max attempts reached for {url}")
                return False, response.status_code
            delay = config['base_delay'] ** attempt
            logging.warning(f"Rate limited at {url}, retrying in {delay}s")
            time.sleep(delay)
            return check_single_username(username, site_info, proxies, config, attempt + 1)
        
        exists = False
        if response.status_code in success_codes:
            exists = True
            if error_string and error_string in response.text:
                exists = False
        
        return exists, response.status_code
    
    except requests.RequestException as e:
        logging.error(f"Error checking {url}: {str(e)}")
        return False, 0

def check_usernames(username, sites, proxies, config):
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=config['max_workers']) as executor:
        future_to_site = {
            executor.submit(check_single_username, username, site_info, proxies, config): site 
            for site, site_info in sites.items()
        }
        
        with tqdm(total=len(sites), desc="Progress") as pbar:
            for future in concurrent.futures.as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    results[site] = future.result()
                except Exception as e:
                    results[site] = (False, 0)
                    logging.error(f"Exception for {site}: {str(e)}")
                pbar.update(1)
    
    return results