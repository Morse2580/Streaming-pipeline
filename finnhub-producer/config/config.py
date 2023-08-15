import logging
from pathlib import Path
from typing import List

import yaml

from src.utils.utils import load_conf


class FinnhubConf:
    """
    Class to manage environment variables and configurations for the FinnhubProducer.

    Attributes:
        finnhub_api_token (str): Finnhub API token retrieved from the configuration file.
        finnhub_stocks_tickers (list): List of stock tickers retrieved from the configuration file.
        finnhub_validate_tickers (bool): Boolean flag indicating whether to validate stock tickers.
    """

    def __init__(self):
        """
        Initialize the Configuration instance by loading configuration values from a YAML file.
        """

        self.conf_file_path = "finnhub-conf.yaml"
        self.load_configuration()

    def load_configuration(self):
        """
        Load configuration values from the YAML file.
        """
        try:
            config_finnhub_values = load_conf(self.conf_file_path)

            # finnhub values
            self.finnhub_api_token = config_finnhub_values.get('FINNHUB_API_TOKEN')
            self.finnhub_stocks_tickers = config_finnhub_values.get('FINNHUB_STOCKS_TICKERS', [])
            self.finnhub_validate_tickers = config_finnhub_values.get('FINNHUB_VALIDATE_TICKERS', False)

        except Exception as e:
            logging.error(f"Error loading configuration: {e}")


