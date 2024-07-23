import pandas as pd

class SubscribeForRealTime:
    def __init__(self, access_token: str, ticker: str, callback: callable) -> None:
        self.access_token: str
        self.ticker: str
        self.url: str
        self.hub_connection: self._build_connection
        self.connected: bool 
        self.callback: callback
        self.list_columns: list
        self.list_columns_int: list
        self.list_columns_float: list
        self.df: pd.DataFrame


    def _data_handler(self, message) -> None: ...
        
    def _build_connection(self) -> _build_connection: ...

    def _receive_message(self, message) -> None: ...

    def _handle_error(self, error) -> None: ...
    
    def _on_connect(self) -> None: ...

    def _on_disconnect(self) -> None: ... 

    def _join_groups(self) -> None: ...

    def _run(self) -> None: ...
        
    def start(self) -> None: ...
        
    def stop(self) -> None: ...

