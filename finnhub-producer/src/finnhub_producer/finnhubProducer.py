from config.config import FinnhubConf
from src.web_socket_manager.finnhub_client import FinnhubClient


class FinnhubProducer:
    """
    Class to ingest upcoming messages from Finnhub WebSocket into the collector API.
    """

    def __init__(
            self, config: FinnhubConf, finnhub_client: FinnhubClient
    ):
        """
        Initialize the FinnhubProducer instance.
        """
        self.finnhub_config = config
        self.finnhub_client = finnhub_client

    def setup(self):
        """
        Set up the FinnhubProducer instance by loading the Finnhub client
        """
        self.finnhub_client = FinnhubClient(self.finnhub_config)

    def start(self):
        """
        Start ingesting upcoming messages by connecting to the WebSocket and logging environment variables.
        """
        self.finnhub_client.connect()

    def stop(self):
        """
        Stop the WebSocket connection.
        """
        self.websocket_manager.close()

