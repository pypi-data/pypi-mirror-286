from apache_bot_blocker.bad_bot_blocker import *
import configparser
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple


def read_config(file_path: str = 'C:/Users/anpei/PycharmProjects/final_bot_blocker/config.ini'):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
    except configparser.Error as e:
        logging.error(f"Error reading config file: {e}")
        raise
    return config


def get_parameters(config):
    try:
        log_file_name = (config['LOG']['log_file_name'])
        log_file_location = config['LOG']['log_file_path']
        log_file_format = config['LOG']['log_file_format']
        timestamp_format = config['LOG']['timestamp_format']
        good_domain_list = eval(config['GOOD_BOT']['good_bot'])
        interval_one = int(config['BOT']['interval_1'])
        interval_two = int(config['BOT']['interval_2'])
        frequency_one = int(config['BOT']['frequency_1'])
        frequency_two = int(config['BOT']['frequency_2'])
        return {"log_file_name": log_file_name, "log_file_location": log_file_location, "log_file_format": log_file_format, "timestamp_format": timestamp_format, "good_domain_list": good_domain_list, "interval_1": interval_one, "interval_2": interval_two, "frequency_1": frequency_one, "frequency_2": frequency_two}

    except (KeyError, ValueError) as e:
        logging.error(f"Error parsing config: {e}")
        raise

def main_function():
    logging.basicConfig(level=logging.INFO)

    try:
        config = read_config()
        params = get_parameters(config)
        print(params)
        print(type(params))
        logging.info(f"Parsed parameters: {params}")

        block_bad_bots(
            params["log_file_name"],
            params["log_file_location"],
            params["log_file_format"],
            params["timestamp_format"],
            params["good_domain_list"],
            params["interval_1"],
            params["interval_2"],
            params["frequency_1"],
            params["frequency_2"]
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")



if __name__ == "__main__":
    main_function()

