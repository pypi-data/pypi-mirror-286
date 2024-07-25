from datetime import datetime
from .FiinIndicator import FiinIndicator
from .AggregatesBars  import IndexBars, TickerBars, DerivativeBars, CoveredWarrantBars
from .SubscribeEvents import SubscribeEvents

class LoginRequiredException: ...

class FiinSession:
    def __init__(self, username: str, password: str):
        self.username: str
        self.password: str
        self.is_login: bool
        self.access_token: str
        self.expired_token: int
        self.urlGetToken: str
        self.bodyGetToken: dict

    def login(self) -> FiinSession: ...
        
    def _is_valid_token(self) -> bool: ...
    
    def FiinIndicator(self) -> FiinIndicator: ...
    
    def IndexBars(self, ticker: str, by: str, from_date: str | datetime, 
                   to_date: str | datetime = datetime.now(), 
                   multiplier: int = 1, limit: int = 1000) -> IndexBars:...
    
    def TickerBars(self, ticker: str, by: str, from_date: str | datetime, 
                   to_date: str | datetime = datetime.now(), 
                   multiplier: int = 1, limit: int = 1000) -> TickerBars:...
    
    def DerivativeBars(self, ticker: str, by: str, from_date: str | datetime, 
                   to_date: str | datetime = datetime.now(), 
                   multiplier: int = 1, limit: int = 1000) -> DerivativeBars:...
    
    def CoveredWarrantBars(self, ticker: str, by: str, from_date: str | datetime, 
                   to_date: str | datetime = datetime.now(), 
                   multiplier: int = 1, limit: int = 1000) -> CoveredWarrantBars:...
    
    def SubscribeEvents(self, data_type: str, ticker: str, 
                        callback: callable) -> SubscribeEvents: ...
 
    
