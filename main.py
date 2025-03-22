from search import check_username
from utils import print_result

def main():
    print("Holmex v0.01 - Username Checker")
    username = input("Enter username to search: ")
    
    # Sample sites to check (just examples)
    sites = {
        "Twitter": "https://twitter.com/",
        "GitHub": "https://github.com/",
        "Instagram": "https://instagram.com/"
    }
    
    print("\nChecking username availability...")
    for site_name, base_url in sites.items():
        result = check_username(username, base_url)
        print_result(site_name, result)

if __name__ == "__main__":
    main()