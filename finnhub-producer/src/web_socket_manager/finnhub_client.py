import json

import finnhub
import websocket
from finnhub import Client

from config.config import *
from src.collector_api.collector import CollectorAPIClient
from src.entities.entity_models import TradeEventMessage


class FinnhubClient:
    """
    Class to manage the WebSocket connection to Finnhub.

    Attributes:
        api_token (str): Finnhub API token for authentication.
    """

    def __init__(
            self,
            config_instance: FinnhubConf,
            collector_api_client: CollectorAPIClient = CollectorAPIClient()
    ):

        websocket.enableTrace(True)
        self.ws = None
        self.api_token = config_instance.finnhub_api_token
        self.tickers = config_instance.finnhub_stocks_tickers
        self.validate = config_instance.finnhub_validate_tickers
        self.collector_api_client = collector_api_client

    def test_connection(self):
        """
        Test the API connection for the Finnhub Web Socket API
        """
        websocket_url = f'wss://ws.finnhub.io?token={self.api_token}'

        print(websocket_url)
        try:
            ws = websocket.create_connection(websocket_url)
            ws.close()
            return 200  # if successful
        except websocket.WebSocketException as e:
            print(f"WebSocket connection failed: {e}")
            return 500  # Internal server error if no connection can be established

    def connect(self):
        """
        Connect to the Finnhub WebSocket server and start listening for messages.
        """
        self.ws = websocket.WebSocketApp(
            f'wss://ws.finnhub.io?token={self.api_token}',
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message):
        """
        Callback function to process incoming messages.

        Args:
            ws: WebSocket instance.
            message (JSON): Incoming message.
        """
        data = json.loads(message)
        trade_event_message = TradeEventMessage(**data)
        self.collector_api_client.post(trade_event_message)

    def on_error(self, ws, error):
        """
        Callback function to handle WebSocket errors.

        Args:
            ws: WebSocket instance.
            error: Error message.
        """
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback function to handle WebSocket closure.

        Args:
            ws: WebSocket instance.
            close_status_code (int): Status code indicating the reason for closure.
            close_msg (str): Closing message.
        """
        print(f"WebSocket closed with status code {close_status_code}: {close_msg}")

    def on_open(
            self, ws
    ):
        for ticker in self.tickers:
            subscription_message = f'{{"type":"subscribe","symbol":"{ticker}"}}'

            if self.validate == "1" and not self.ticker_validator(self.load_client(), ticker):
                print(f'Subscription for {ticker} failed - ticker not found')
                continue

            self.send_subscription(subscription_message)

            if self.validate == "1":
                print(f'Subscription for {ticker} succeeded')

    def send_subscription(
            self, subscription_data
    ):
        """
        Send subscription data to the WebSocket server.

        Args:
            subscription_data (str): Subscription data to be sent.
        """
        self.ws.send(subscription_data)

    def load_client(self):
        return finnhub.Client(api_key=self.api_token)

    def lookup_ticker(
            self, finnhub_client: Client, ticker
    ):
        return finnhub_client.symbol_lookup(ticker)

    def ticker_validator(
            self, finnhub_client: Client, ticker
    ):
        for stock in self.lookup_ticker(finnhub_client, ticker)['result']:
            if stock['symbol'] == ticker:
                return True
        return False
