def print_result(site_name, exists):
    status = "Found" if exists else "Not Found"
    print(f"{site_name}: {status}")