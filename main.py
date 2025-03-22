import json
import logging
from search import check_usernames
from utils import print_result, print_summary, save_results

# Setup basic logging
logging.basicConfig(
    filename='holmex.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("Holmex v0.03 - Username Checker")
    username = input("Enter username to search: ")
    
    try:
        with open('sites.json', 'r') as f:
            sites = json.load(f)
    except FileNotFoundError:
        print("Error: sites.json not found!")
        logging.error("sites.json not found")
        return
    
    print("\nChecking username availability across sites...")
    logging.info(f"Starting username check for: {username}")

    results = check_usernames(username, sites)
    
    for site_name, result in results.items():
        print_result(site_name, result)
    
    print_summary(results)

    # Save results
    save_results(username, results)
    logging.info(f"Completed check for {username}")

if __name__ == "__main__":
    main()