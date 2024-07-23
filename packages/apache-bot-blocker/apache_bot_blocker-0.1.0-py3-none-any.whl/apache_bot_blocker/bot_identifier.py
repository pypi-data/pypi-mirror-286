import socket
import multiprocessing
import logging
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotIdentify:

    GOOD_DOMAIN_LIST: Dict[str, List[str]] = {}

    def __init__(self, ip):
        self.ip = ip
        self.bot_list: List[str] = []

    def reverse_dns_lookup(self, queue: multiprocessing.Queue):
        """Perform a reverse DNS lookup and put the result in the queue."""
        try:
            host_name, _, _ = socket.gethostbyaddr(self.ip)
            logger.info(f"IP is: {self.ip}, host_name is {host_name}")
            queue.put(host_name)
        except (socket.herror, socket.timeout) as e:
            logger.error(f"Error in reverse DNS lookup: {e}")
            queue.put(None)

    def reverse_dns_with_timeout(self, timeout: float) -> Optional[str]:
        """
        Perform a Reverse DNS Lookup with a Timeout

        Args:
            timeout (float): The timeout in seconds.

        Returns:
            Optional[str]: The hostname if found, None otherwise.
        """
        queue = multiprocessing.Queue()
        rdl_process = multiprocessing.Process(target=self.reverse_dns_lookup, name="Reverse_DNS_Lookup", args=(queue,))
        rdl_process.start()
        rdl_process.join(timeout)
        if rdl_process.is_alive():
            rdl_process.terminate()
            rdl_process.join()
            logger.warning("Reverse DNS lookup timed out")
            return None
        return queue.get()

    def forward_dns_lookup(self, hostname: str) -> Optional[List[str]]:
        """
        Performs a Forward DNS Lookup

        Args:
            hostname (str): The hostname to look up.

        Returns:
            Optional[List[str]]: List of IP addresses if found, None otherwise.
        """
        try:
            return socket.gethostbyname_ex(hostname)[2]
        except socket.gaierror as e:
            logger.error(f"Error in forward DNS lookup: {e}")
            return None

    def is_good_bot(self, timeout: float) -> bool:
        """
        Check if the IP belongs to a good bot.

        Args:
            timeout (float): The timeout for reverse DNS lookup in seconds.

        Returns:
            bool: True if it's a good bot, False otherwise.
        """
        hostname = self.reverse_dns_with_timeout(timeout)
        if hostname:
            for bot, domains in self.GOOD_DOMAIN_LIST.items():
                if any(hostname.endswith(domain) for domain in domains):
                    verified_ips = self.forward_dns_lookup(hostname)
                    if self.ip in verified_ips:
                        self.bot_list.append(self.ip)
                        logger.info(f"Good bot identified: {bot} - {self.ip}")
                        return True
        logger.info(f"Not a good bot: {self.ip}")
        return False
