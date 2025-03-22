import json
from datetime import datetime

def print_result(site_name, exists, status):
    status_symbol = "✓" if exists else "✗"
    print(f"{site_name}: {status_symbol} (HTTP {status})")

def print_summary(results):
    found = sum(1 for exists, _ in results.values() if exists)
    total = len(results)
    print(f"\nSummary: Found on {found}/{total} sites")

def save_results(username, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{username}_{timestamp}.json"
    
    result_data = {
        "username": username,
        "timestamp": timestamp,
        "results": {site: {"exists": exists, "status": status} 
                   for site, (exists, status) in results.items()}
    }
    
    with open(filename, 'w') as f:
        json.dump(result_data, f, indent=4)
    print(f"\nResults saved to {filename}")