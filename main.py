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
    parser = argparse.ArgumentParser(description="Holmex v0.04 - Username Checker")
    parser.add_argument("username", help="Username to search for")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://proxy:port)")
    args = parser.parse_args()

    print(f"Holmex v0.04 - Checking username: {args.username}")
    
    try:
        with open('sites.json', 'r') as f:
            sites = json.load(f)
    except FileNotFoundError:
        print("Error: sites.json not found!")
        logging.error("sites.json not found")
        return
    
    print(f"\nChecking {len(sites)} sites...")
    logging.info(f"Starting username check for: {args.username}")
    
    results = check_usernames(args.username, sites, args.proxy)
    
    for site_name, result in results.items():
        print_result(site_name, result)
    
    print_summary(results)
    save_results(args.username, results)
    logging.info(f"Completed check for {args.username}")

if __name__ == "__main__":
    main()