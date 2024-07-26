import time
import requests
from datetime import datetime
from .FiinIndicator import FiinIndicator
from .Aggregates import IndexBars, TickerBars, CoveredWarrantBars, DerivativeBars
from .SubscribeDerivativeEvents import SubscribeDerivativeEvents
from .SubscribeCoveredWarrantEvents import SubscribeCoveredWarrantEvents
from .SubscribeIndexEvents import SubscribeIndexEvents
from .SubscribeTickerEvents import SubscribeTickerEvents


TOKEN_URL = "http://42.112.22.11:9900/connect/token"
GRANT_TYPE = 'password'
CLIENT_ID = 'FiinTrade.Customer.Client'
CLIENT_SECRET = 'fiintrade-Cus2023'
SCOPE = 'openid fiintrade.customer'
USERNAME = ''
PASSWORD = ''

class FiinSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_login = False
        self.access_token = None
        self.expired_token = None
        self.urlGetToken = TOKEN_URL
        self.bodyGetToken = {
            'grant_type': GRANT_TYPE,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': SCOPE,
            'username': USERNAME,
            'password': PASSWORD
        }

    def _is_valid_token(self): 
        if self.access_token is None:
            return False
        expires_in = self.expired_token
        current_time = int(time.time())
        try:
            if expires_in <= current_time:  
                return True       
            else: 
                return False
        except:
            return False    
    def login(self):
        if self._is_valid_token():
            self.is_login = True
            return self
        else:
            self.bodyGetToken['username'] = self.username
            self.bodyGetToken['password'] = self.password
            try:
                response = requests.post(self.urlGetToken, data=self.bodyGetToken)
                if response.status_code == 200:
                    res = response.json()
                    self.access_token = res['access_token']
                    self.expired_token = res['expires_in'] + int(time.time())
                    self.is_login = True
                    return self
                else:
                    res = response.json()
                    print(res['error_description'])
                    self.is_login = False  
                    raise NameError("Login failed")
                
            except:
                self.is_login = False
                return self
   
    def FiinIndicator(self):
        if self.is_login:
            return FiinIndicator()
        else:
            raise NameError("Please login before calling data")
        
    def IndexBars(self, ticker: str, by: str, from_date: str | datetime, 
                           to_date: str | datetime, multiplier: int = 1, limit: int = 1000):
        if self.is_login:
            return IndexBars(self.access_token, ticker, by, 
                             from_date, to_date, multiplier, limit)
        else:
            raise NameError("Please login before calling data")
        
    def TickerBars(self, ticker: str, by: str, from_date: str | datetime, 
                           to_date: str | datetime, multiplier: int = 1, limit: int = 1000):
        if self.is_login:
            return TickerBars(self.access_token, ticker, by, 
                             from_date, to_date, multiplier, limit)
        else:
            raise NameError("Please login before calling data")
        
        
    def CoveredWarrantBars(self, ticker: str, by: str, from_date: str | datetime, 
                           to_date: str | datetime, multiplier: int = 1, limit: int = 1000):
        if self.is_login:
            return CoveredWarrantBars(self.access_token, ticker, by, 
                             from_date, to_date, multiplier, limit)
        else:
            raise NameError("Please login before calling data")
        
    def DerivativeBars(self, ticker: str, by: str, from_date: str | datetime, 
                           to_date: str | datetime, multiplier: int = 1, limit: int = 1000):
        if self.is_login:
            return DerivativeBars(self.access_token, ticker, by, 
                             from_date, to_date, multiplier, limit)
        else:
            raise NameError("Please login before calling data")

## SubscribeEvents
    def SubscribeDerivativeEvents(self, ticker: str, callback: callable):
        if self.is_login:
            return SubscribeDerivativeEvents(self.access_token, ticker, callback)
        else:
            raise NameError("Please login before calling data")
    def SubscribeCoveredWarrantEvents(self, ticker: str, callback: callable):
        if self.is_login:
            return SubscribeCoveredWarrantEvents(self.access_token, ticker, callback)
        else:
            raise NameError("Please login before calling data")
    def SubscribeTickerEvents(self, ticker: str, callback: callable):
        if self.is_login:
            return SubscribeTickerEvents(self.access_token, ticker, callback)
        else:
            raise NameError("Please login before calling data")
    def SubscribeIndexEvents(self, ticker: str, callback: callable):
        if self.is_login:
            return SubscribeIndexEvents(self.access_token, ticker, callback)
        else:
            raise NameError("Please login before calling data")

     

