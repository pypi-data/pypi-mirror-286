import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project root
project_root = os.path.dirname(current_dir)

# Construct paths to whitelist and blacklist
whitelist_path = os.path.join(project_root, 'whitelist')
blacklist_path = os.path.join(project_root, 'blacklist')


def read_ip_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


whitelisted_ips = read_ip_list(whitelist_path)
blacklisted_ips = read_ip_list(blacklist_path)