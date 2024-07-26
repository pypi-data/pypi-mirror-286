import numpy as np
import pandas as pd


class FiinIndicator:
    def ema(self, 
            col: pd.Series, 
            window: int):
        
        ema = col.ewm(span=window, min_periods=window, adjust=False).mean()
        return ema
            
    def sma(self, 
            col: pd.Series, 
            window: int):
        
        sma = col.rolling(window=window, min_periods=window).mean()
        return sma
    
    def rsi(self, 
            col: pd.Series, 
            window: int = 14):
        
        col = col.astype(int)
        delta = col.diff()
        gain = delta.where(delta > 0, 0) 
        loss = -delta.where(delta < 0, 0) 
        avg_gain = gain.ewm(com=window - 1, min_periods=window, adjust=False).mean() 
        avg_loss = loss.ewm(com=window - 1, min_periods=window, adjust=False).mean() 
        rs = avg_gain / avg_loss.abs() 
        rsi = 100 - (100 / (1 + rs)) 
        rsi[(avg_loss == 0) | (avg_loss == -avg_gain)] = 100  
        return rsi
    
    def macd(self, 
             col: pd.Series, 
             window_slow: int = 26, 
             window_fast: int = 12):
                 
        ema_fast = self.ema(col, window_fast)
        ema_slow = self.ema(col, window_slow)
        macd_line = ema_fast - ema_slow
        return macd_line

    def macd_signal(self, 
                    col: pd.Series, 
                    window_slow: int = 26, 
                    window_fast: int = 12, 
                    window_sign: int = 9):
        
        macd = self.macd(col, window_slow, window_fast)
        macd_signal_line = self.ema(macd, window_sign)
        return macd_signal_line

    def macd_diff(self, 
                  col: pd.Series, 
                  window_slow: int = 26, 
                  window_fast: int = 12, 
                  window_sign: int = 9):
        
        macd = self.macd(col, window_slow, window_fast)
        macd_signal = self.macd_signal(col, window_slow, window_fast, window_sign)
        macd_diff_line = macd - macd_signal
        return macd_diff_line

    def bollinger_mavg(self, 
                       col: pd.Series, 
                       window: int = 20):
        
        bollinger_mavg = self.sma(col, window)
        return bollinger_mavg

    def bollinger_std(self, 
                      col: pd.Series, 
                      window: int = 20):
        
        try:
            rolling_windows = np.lib.stride_tricks.sliding_window_view(col, window)
            stds = np.std(rolling_windows, axis=1)
            stds = np.concatenate([np.full(window - 1, np.nan), stds])
            std = pd.Series(stds, index=col.index)
            return std
        except:
            std = pd.Series([np.nan] * col.shape[0])
            return std

    def bollinger_hband(self, 
                        col: pd.Series, 
                        window: int = 20, 
                        window_dev = 2):
        
        sma_bb = self.sma(col, window)
        std_bb = self.bollinger_std(col, window)
        bollinger_hband = sma_bb + (window_dev * std_bb)
        return bollinger_hband

    def bollinger_lband(self, 
                        col: pd.Series, 
                        window: int = 20, 
                        window_dev = 2):
        
        sma_bb = self.sma(col, window)
        std_bb = self.bollinger_std(col, window)
        bollinger_lband = sma_bb - (window_dev * std_bb)
        return bollinger_lband
    
    def stoch(self, 
              low: pd.Series, 
              high: pd.Series, 
              close: pd.Series, 
              window: int = 14):
        
        lowest_low = low.rolling(window=window).min()
        highest_high = high.rolling(window=window).max()
        stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        return stoch_k

    def stoch_signal(self, 
                     low: pd.Series, 
                     high: pd.Series, 
                     close: pd.Series, 
                     window: int = 14, 
                     smooth_window: int = 3):
        
        stoch_k = self.stoch(low, high, close, window)
        stoch_d = self.sma(stoch_k, smooth_window)
        return stoch_d
    
