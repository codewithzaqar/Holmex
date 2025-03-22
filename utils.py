import json
from datetime import datetime

def print_result(site_name, exists):
    status = "✓ Found" if exists else "✗ Not Found"
    print(f"{site_name}: {status}")

def print_summary(results):
    found = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"\nSummary: Found on {found}/{total} sites")

def save_results(username, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{username}_{timestamp}.json"

    result_data = {
        "username": username,
        "timestamp": timestamp,
        "results": results
    }

    with open(filename, 'w') as f:
        json.dump(result_data, f, indent=4)
    print(f"\nResults saved to {filename}")