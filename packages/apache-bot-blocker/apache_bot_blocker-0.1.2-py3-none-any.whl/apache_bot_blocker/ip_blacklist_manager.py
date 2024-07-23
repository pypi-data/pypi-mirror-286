import subprocess
import re
import logging
from typing import List, Optional


IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')


def is_valid_ip(ip: str) -> bool:
    """Validate an IP address"""
    if IP_PATTERN.match(ip):
        return all(0 <= int(part) <= 255 for part in ip.split('.'))
    return False


class BlackListManager:
    """BlackListManager is responsible for managing a list of IP addresses to be blacklisted on a linux remote server firewall。 Internally uses Linux commands iptables/ipset
    This class provides functionalities to:

    1. Create an ip list
    2. Check if IP list exists
    3. Add an IP to the IP list
    4. Add a rule blocking the blacklist
    5. Displaying all results"""

    IPLIST_NAME = 'dp_blacklist'

    def __init__(self, ip_list_file):
        self.ip_list_file = ip_list_file
        self.valid_ip_count = 0
        self.ips_in_ipset = 0
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def list_exists(self) -> bool:
        """Check if the IP list exists in ipset."""
        try:
            result = subprocess.run(['sudo', 'ipset', 'list', self.IPLIST_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            exists = "Name:" in result.stdout
            self.logger.info(f"{self.IPLIST_NAME} {'already exists' if exists else 'can be created'}")
            return exists
        except subprocess.CalledProcessError:
            self.logger.error(f"Error checking if {self.IPLIST_NAME} exists")
            return False

    def create_iplist(self) -> None:
        """Create the IP list in ipset if it doesn't exist."""
        if not self.list_exists():
            try:
                subprocess.run(['sudo', 'ipset', 'create', self.IPLIST_NAME, 'hash:ip'], check=True)
                self.logger.info(f"{self.IPLIST_NAME} has been created in the ipset")
            except subprocess.CalledProcessError:
                self.logger.error(f"Error creating {self.IPLIST_NAME}")
        return

    def get_ipset_entries(self) -> int:
        """Get the number of entries in the ipset."""
        try:
            result = subprocess.run(['sudo', 'ipset', 'list', self.IPLIST_NAME], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if line.startswith('Number of entries:'):
                    return int(line.split(':')[1].strip())
        except subprocess.CalledProcessError:
            self.logger.error(f"Error getting entries for {self.IPLIST_NAME}")
        return 0

    def add_ip_ipset(self):
        """Add IPs from the file to the ipset."""
        initial_entries = self.get_ipset_entries()
        self.logger.info(f"{initial_entries} IPs are in this list initially")

        with open(self.ip_list_file, 'r') as file:
            for ip in file:
                stripped_ip = ip.strip()
                if is_valid_ip(stripped_ip):
                    self.valid_ip_count += 1
                    result = subprocess.run(['sudo', 'ipset', 'test', self.IPLIST_NAME.encode(), stripped_ip.encode()],
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if "is NOT in set" in result.stderr:
                        subprocess.run(['sudo', 'ipset', 'add', self.IPLIST_NAME.encode(), stripped_ip.encode()])
                        self.logger.info(f"{ip} added")
                    else:
                        self.logger.info(f"{ip} already in {self.IPLIST_NAME}")
        self.ips_in_ipset = self.get_ipset_entries()

    def rule_exists(self):
        """Check if the iptables rule for the ipset exists."""
        try:
            result = subprocess.run(['sudo', 'iptables', '-S'], capture_output=True, text=True, check=True)
            for rule in result.stdout.splitlines():
                if f"INPUT -m set --match-set {self.IPLIST_NAME} " in rule and "DROP" in rule:
                    self.logger.info(f"{self.IPLIST_NAME} rule already exists")
                    return True
        except subprocess.CalledProcessError:
            self.logger.error("Error checking iptables rules")
        return False

    def add_rule(self):
        """Add the iptables rule for the ipset if it doesn't exist."""
        if not self.rule_exists():
            try:
                subprocess.run(
                    ['sudo', 'iptables', '-I', 'INPUT', '-m', 'set', '--match-set', self.IPLIST_NAME.encode(), 'final_bot_blocker', '-j', 'DROP'])
                self.logger.info("Added rule")
            except subprocess.CalledProcessError:
                self.logger.error("Error adding iptables rule")

    def display_iptables_rules(self) -> None:
        """Display created iptables rules."""
        try:
            result = subprocess.run(['sudo', 'iptables', '-S'], capture_output=True, text=True, check=True)
            relevant_rules = [rule for rule in result.stdout.splitlines() if f"match-set {self.IPLIST_NAME} " in rule]
            for rule in relevant_rules:
                self.logger.info(rule)
        except subprocess.CalledProcessError:
            self.logger.error("Error displaying iptables rules")

    def display_results(self):
        """Display the results of the blacklist operations."""
        self.display_iptables_rules()
        self.logger.info(f"Valid IP count in document: {self.valid_ip_count}")
        self.logger.info(f"IPs in {self.IPLIST_NAME}: {self.ips_in_ipset}")

    def block_ips(self):
        """Main method to execute the blacklist creation and population."""
        self.create_iplist()
        self.add_ip_ipset()
        self.add_rule()
        self.display_results()


