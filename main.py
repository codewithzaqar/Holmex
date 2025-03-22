import json
from search import check_usernames
from utils import print_result, print_summary

def main():
    print("Holmex v0.02 - Username Checker")
    username = input("Enter username to search: ")
    
    # Load sites from config file
    try:
        with open('sites.json', 'r') as f:
            sites = json.load(f)
    except FileNotFoundError:
        print("Error: sites.json not found!")
        return
    
    print("\nChecking username availability across sites...")
    results = check_usernames(username, sites)
    
    # Display results
    for site_name, result in results.items():
        print_result(site_name, result)
    
    print_summary(results)

if __name__ == "__main__":
    main()