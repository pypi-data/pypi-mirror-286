from datetime import datetime
import pandas as pd
import requests

HISTORICAL_API = "https://fiinquant-staging.fiintrade.vn/TradingView/GetStockChartData"


class BarData:
    def __init__(self, data):
        self.__private_attribute = data
        self.Open = data.Open
        self.Low = data.Low
        self.High = data.High
        self.Close = data.Close
        self.Volume = data.Volume
        self.Timestamp = data.Timestamp

    def to_dataFrame(self):
        return self.__private_attribute

class Bar:
    def __init__(self, 
                 access_token: str, 
                 ticker: str,  
                 by: str,  
                 from_date: str | datetime,  
                 to_date: str | datetime,  
                 multiplier: int = 1,  
                 limit: int = 1000):
        
        self.access_token = access_token
        self.ticker = ticker
        self.by = by
        if self.by not in ['MINUTES', 'HOURS', 'DAYS']:
            raise ValueError('Invalid value for "by". Must be one of MINUTES, HOURS, DAYS')
        
        self.from_date = from_date
        if isinstance(self.from_date, datetime):
            self.from_date = self.from_date.strftime('%Y-%m-%d %H:%M:%S')
        self.to_date = to_date
        if isinstance(self.to_date, datetime):
            self.to_date = self.to_date.strftime('%Y-%m-%d %H:%M:%S')
        self.multiplier = multiplier
        self.limit = limit
        self.urlGetDataStock = HISTORICAL_API
        self.convertTime = {
            'MINUTES': 'EachMinute',
            'HOURS': 'EachOneHour',
            'DAYS': 'Daily',
        }

    def _fetch_historical_data(self, data_type: str):
        # Define the parameters for the API request
        param = {
            'Code' : self.ticker, 
            'Type' : data_type, # Stock, Index, CoveredWarrant, Derivative
            'Frequency' : self.convertTime[self.by], # EachMinute, EachOneHour, Daily
            'From' : self.from_date,
            'To' : self.to_date,
            'PageSize' : self.limit
        }
        # Make the API request
        response = requests.get(
            url=self.urlGetDataStock, 
            params=param, 
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        if response.status_code == 200:
            res = response.json()
            df = pd.DataFrame(res['items'])
            return df
        else:
            response.raise_for_status()

    def _preprocess_data(self):
        # Drop unnecessary columns
        self.df = self.df.drop(columns=['rateAdjusted', 'openInterest'])

        # Rename columns to standard names
        self.df = self.df.rename(columns={
            "tradingDate": "Timestamp", 
            "openPrice": "Open", 
            "lowestPrice": "Low", 
            "highestPrice": "High", 
            "closePrice": "Close", 
            "totalMatchVolume": "Volume", 
        })

        # Format columns
        self.df[['Open', 'Low', 'High', 'Close', 'Volume']] = self.df[['Open', 'Low', 'High', 'Close', 'Volume']].astype(int)
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], format='ISO8601')
        
        if self.by == 'HOURS':
            self.df['Timestamp'] = self.df['Timestamp'].apply(lambda x: x.replace(second=0, microsecond=0))

        # Group data by multiplier
        self.df['group'] = (self.df.index // self.multiplier)
        self.df = self.df.groupby('group').agg({
            'Timestamp': 'first',
            'Open': 'first',     
            'High': 'max',       
            'Low': 'min',        
            'Close': 'last',     
            'Volume': 'sum'
        }).reset_index(drop=True)
        
        return self.df

    def get(self, data_type: str):
        self.df = self._fetch_historical_data(data_type)
        self.df = self._preprocess_data()
        return BarData(self.df)


class IndexBars(Bar):
    def get(self):
        return super().get('Index')

class TickerBars(Bar):
    def get(self):
        return super().get('Stock')

class CoveredWarrantBars(Bar):
    def get(self):
        return super().get('CoveredWarrant')
    
class DerivativeBars(Bar):
    def get(self):
        return super().get('Derivative')



