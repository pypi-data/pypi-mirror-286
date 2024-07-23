from datetime import datetime
from .FiinIndicator import FiinIndicator
from .FiinDataHistorical import FiinDataHistorical
from .SubscribeForRealTime import SubscribeForRealTime

class FiinSession:
    def __init__(self, username: str, password: str):

        self.username: str
        self.password: str
        self.is_login: bool
        self.access_token: str
        self.expired_token: int
        self.urlGetToken: str
        self.bodyGetToken: dict

    def _login(self) -> None: ...
        
    def _is_expired_token(self) -> bool: ...

    def _get_access_token(self) -> str: ...
        
    def FiinDataHistorical(self, 
                           ticker: str, 
                           from_date: str | datetime = '2000-01-01 00:00:00', 
                           to_date: str | datetime = datetime.now(), 
                           multiplier: int = 1, 
                           timespan: str = 'minute', 
                           limit: int = 1000) -> FiinDataHistorical: ...
   
    def FiinIndicator(self) -> FiinIndicator: ...
    
    def SubscribeForRealTime(self, 
                             ticker: str, 
                             callback: callable) -> SubscribeForRealTime: ...


