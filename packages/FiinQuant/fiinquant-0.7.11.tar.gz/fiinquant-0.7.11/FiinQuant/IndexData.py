        
class IndexData:
    def __init__(self,data):
        self.__private_attribute = data
        self.TotalMatchVolume = data['TotalMatchVolume']
        self.MarketStatus = data['MarketStatus']
        self.TradingDate = data['TradingDate']
        self.ComGroupCode = data['ComGroupCode']
        self.ReferenceIndex = data['ReferenceIndex']
        self.OpenIndex = data['OpenIndex']
        self.CloseIndex = data['CloseIndex']
        self.HighestIndex = data['HighestIndex']
        self.LowestIndex = data['LowestIndex']
        self.IndexValue = data['IndexValue']
        self.IndexChange = data['IndexChange']
        self.PercentIndexChange = data['PercentIndexChange']
        self.MatchVolume = data['MatchVolume']
        self.MatchValue = data['MatchValue']
        self.TotalMatchValue = data['TotalMatchValue']  
        self.TotalDealVolume = data['TotalDealVolume']
        self.TotalDealValue = data['TotalDealValue']
        self.TotalStockUpPrice = data['TotalStockUpPrice']
        self.TotalStockDownPrice = data['TotalStockDownPrice']
        self.TotalStockNoChangePrice = data['TotalStockNoChangePrice']
        self.TotalStockOverCeiling = data['TotalStockOverCeiling']
        self.TotalStockUnderFloor = data['TotalStockUnderFloor']
        self.ForeignBuyVolumeTotal = data['ForeignBuyVolumeTotal']
        self.ForeignBuyValueTotal = data['ForeignBuyValueTotal']
        self.ForeignSellVolumeTotal = data['ForeignSellVolumeTotal']
        self.ForeignSellValueTotal = data['ForeignSellValueTotal']
        self.VolumeBu = data['VolumeBu']
        self.VolumeSd = data['VolumeSd']
    def get_data(self):
        return self.__private_attribute 
    