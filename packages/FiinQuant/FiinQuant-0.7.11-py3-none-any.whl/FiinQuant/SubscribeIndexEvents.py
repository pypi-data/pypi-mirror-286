import time
import threading
import pandas as pd
from signalrcore.hub_connection_builder import HubConnectionBuilder
from .IndexData import IndexData


REALTIME_API = "https://fiinquant-realtime-staging.fiintrade.vn/RealtimeHub?access_token="

class SubscribeIndexEvents:
    def __init__(self, access_token: str, ticker: str, callback: callable):
        self.url = REALTIME_API
        self.hub_connection = self._build_connection()
        self.connected = False 
        self.callback = callback
        self.access_token = access_token
        self.df_index = pd.DataFrame(columns=[
            'TotalMatchVolume', 'MarketStatus', 'TradingDate', 'ComGroupCode','ReferenceIndex',
            'OpenIndex','CloseIndex','HighestIndex','LowestIndex','IndexValue','IndexChange','PercentIndexChange','MatchVolume','MatchValue',
            'TotalMatchValue','TotalDealVolume','TotalDealValue','TotalStockUpPrice','TotalStockDownPrice','TotalStockNoChangePrice',
            'TotalStockOverCeiling','TotalStockUnderFloor','ForeignBuyVolumeTotal','ForeignBuyValueTotal',
            'ForeignSellVolumeTotal','ForeignSellValueTotal','VolumeBu','VolumeSd'])
        self.ticker = ticker
        self._stop_event = threading.Event()
    def _data_handler(self, message):
        if message is not None:
            self.df_index.loc[len(self.df_index)] = message[0]['data'][0].split('|')
            self.return_data = IndexData(self.df_index[-1:])
            if self.callback:
                self.callback(self.return_data)
        else:
            print("No data received")
            
    def _build_connection(self):
        return HubConnectionBuilder()\
            .with_url(self.url, options={
                "access_token_factory": lambda: self.access_token
            })\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 1,
                "reconnect_interval": [1, 3, 5, 7, 11]
            }).build()

    def _receive_message(self, message):
        self._data_handler(message)

    def _handle_error(self, error):
        print(f"Error: {error}")

    def _on_connect(self):
        self.connected = True
        print("Connection established")
        self._join_groups()

    def _on_disconnect(self):
        self.connected = False
        print("Disconnected from the hub")

    def _join_groups(self):
        if self.connected:
            self.hub_connection.send("JoinGroup", [f"Realtime.Index.{self.ticker}"])
            print(f"Joined group: Realtime.Index.{self.ticker}")
        else:
            raise ValueError("Cannot join groups, not connected")

    def _run(self):
        if self.hub_connection.transport is not None:
            self.hub_connection.stop()

        self.hub_connection.on("ReceiveMessage", self._receive_message)
        self.hub_connection.on_close(self._handle_error)
        self.hub_connection.on_open(self._on_connect)
        self.hub_connection.on_close(self._on_disconnect)
        self.hub_connection.start()
        
        while not self._stop_event.is_set():
           time.sleep(0.5)
        
    def start(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        
    def stop(self):
        self._stop_event.set()
        if self.connected:
            print("Disconnecting...")
            self.hub_connection.stop()
        self.thread.join()
        
