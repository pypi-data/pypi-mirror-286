from datetime import datetime, timedelta
import pandas as pd
from .HistoricalReturnData import HistoricalReturnData

class FiinDataHistorical:
    def __init__(self,
                 access_token: str,
                 ticker: str, 
                 from_date: str | datetime, 
                 to_date: str | datetime, 
                 multiplier: int, 
                 timespan: str, 
                 limit: int):
        
        self.access_token: str
        self.ticker: str
        self.from_date: str | datetime
        self.to_date: str | datetime
        self.multiplier: int
        self.timespan: str
        self.limit: int
        self.urlGetDataStock: str
        self.data: pd.DataFrame

    def _fetch_historical_data(self) -> pd.DataFrame: ...
        
    def _preprocess_data(self) -> pd.DataFrame: ...
    
    def _round_time(self, dt, start_time) -> str: ...
        
    def _group_by_data(self) -> pd.DataFrame: ...

    def _format_data(self) -> pd.DataFrame: ...
    
    def get_data(self) -> HistoricalReturnData: ...

