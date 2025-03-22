def print_result(site_name, exists):
    status = "✓ Found" if exists else "✗ Not Found"
    print(f"{site_name}: {status}")

def print_summary(results):
    found = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"\nSummary: Found on {found}/{total} sites")