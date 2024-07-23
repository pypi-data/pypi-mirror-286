import re
from datetime import datetime, timedelta
import os
import gzip
import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Log2Blacklist:
    class VisitorLog:
        def __init__(self):
            self.information = {}

        def add_info(self, ip, timestamp):
            if ip in self.information:
                self.information[ip].append(timestamp)
            else:
                self.information[ip] = [timestamp]

    def __init__(self):
        self.ip_visit_timestamp = self.VisitorLog()
        self.blacklist_candidates = []

    def read_apache_log(self, filename: str, log_file_path: str, log_file_format: str, timestamp_format: str):
        """Read and parse the Apache log file."""
        line_count = 0
        os.chdir(log_file_path)
        log_pattern = re.compile(rf'{log_file_format}')
        try:
            with gzip.open(filename, 'rb') as apache_log:
                for line in apache_log:
                    line = line.decode('utf-8')
                    pattern_match = log_pattern.match(line)
                    if pattern_match:
                        line_count += 1
                        ip = pattern_match.group('ip')
                        timestamp_str = pattern_match.group('timestamp')
                        timestamp = datetime.strptime(timestamp_str, f'{timestamp_format}')
                        self.ip_visit_timestamp.add_info(ip, timestamp)
                        if line_count % 20000 == 0:
                            print(line_count)
                            if line_count == 1000000:
                                break
        except IOError as e:
            logger.error(f"Error reading log file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        return self.ip_visit_timestamp

    def is_frequent_visitor(self, times: List[datetime], interval_one: int, interval_two: int, frequency_one: int, frequency_two: int):
        """Check if a visitor is frequent based on given criteria."""
        first_cond = False
        second_cond = False
        for i in range(len(times)):
            if i + frequency_one < len(times) and (times[i + frequency_one] - times[i]) <= timedelta(seconds=interval_one):
                first_cond = True
            if i + frequency_two < len(times) and (times[i + frequency_two] - times[i]) <= timedelta(seconds=interval_two):
                second_cond = True
            if first_cond and second_cond:
                return True
        return False

    def check_frequencies(self, first_interval: int, second_interval: int, first_freq: int, second_freq: int):
        """Check frequencies of visits and identify potential blacklist candidates."""
        for ip, times in self.ip_visit_timestamp.information.items():
            if self.is_frequent_visitor(times, first_interval, second_interval, first_freq, second_freq):
                self.blacklist_candidates.append(ip)
                with open("second_copy.txt", "w") as file:
                    file.write(ip)
        # print(count)
        logger.info(f"Found {len(self.blacklist_candidates)} blacklist candidates")
        return self.blacklist_candidates
