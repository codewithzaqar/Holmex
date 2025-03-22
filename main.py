import argparse
import json
import logging
from search import check_usernames
from utils import print_result, print_summary, save_results

logging.basicConfig(
    filename='holmex.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    parser = argparse.ArgumentParser(description="Holmex v0.05 - Username Checker")
    parser.add_argument("username", help="Username to search for")
    parser.add_argument("--proxy", help="Single proxy URL (overrides config)")
    args = parser.parse_args()

    print(f"Holmex v0.05 - Checking username: {args.username}")
    
    # Load config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found!")
        logging.error("config.json not found")
        return
    
    # Load sites
    try:
        with open('sites.json', 'r') as f:
            sites = json.load(f)
    except FileNotFoundError:
        print("Error: sites.json not found!")
        logging.error("sites.json not found")
        return
    
    proxies = [args.proxy] if args.proxy else config.get('proxies', [])
    print(f"\nChecking {len(sites)} sites with {len(proxies) or 'no'} proxies...")
    logging.info(f"Starting username check for: {args.username}")
    
    results = check_usernames(args.username, sites, proxies, config)
    
    for site_name, (exists, status) in results.items():
        print_result(site_name, exists, status)
    
    print_summary(results)
    save_results(args.username, results)
    logging.info(f"Completed check for {args.username}")

if __name__ == "__main__":
    main()