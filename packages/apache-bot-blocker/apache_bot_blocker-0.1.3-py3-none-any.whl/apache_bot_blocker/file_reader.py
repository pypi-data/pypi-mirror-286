# import os
# import sys
#
# def get_config_path():
#     # Paths where config might be found during development and after installation
#     possible_paths = [
#         sys.prefix,  # Installed path
#         os.path.dirname(__file__),  # Development path
#     ]
#     for path in possible_paths:
#         if os.path.exists(os.path.join(path, 'config.ini')):  # Check for the config.ini file
#             return path
#     raise FileNotFoundError('Config directory not found.')
#
# config_dir = get_config_path()
# whitelist_path = os.path.join(config_dir, 'whitelist')
# blacklist_path = os.path.join(config_dir, 'blacklist')
# config_path = os.path.join(config_dir, 'config.ini')
#
# def read_ip_list(file_path):
#     with open(file_path, 'r') as file:
#         return file.read().splitlines()
#
# whitelisted_ips = read_ip_list('/apache_bot_blocker/whitelist')
# blacklisted_ips = read_ip_list('/apache_bot_blocker/blacklist')
import pkg_resources

def read_ip_list(resource_name):
    # Get the resource path
    data = pkg_resources.resource_string(__name__, resource_name)
    return data.decode('utf-8').splitlines()

# Access files included in the package
whitelisted_ips = read_ip_list('whitelist')
blacklisted_ips = read_ip_list('blacklist')
config_file = pkg_resources.resource_filename(__name__, 'config.ini')