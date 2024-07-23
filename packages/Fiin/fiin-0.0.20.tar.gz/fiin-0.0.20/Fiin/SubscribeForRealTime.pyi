import pandas as pd

class RealTimeReturnData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.__private_attribute: pd.DataFrame = data
        self.TotalMatchVolume: int
        self.MarketStatus: str
        self.TradingDate: str
        self.MatchType: str
        self.ComGroupCode: str
        self.OrganCode: str
        self.Ticker: str
        self.ReferencePrice: float
        self.OpenPrice: float
        self.ClosePrice: float
        self.CeilingPrice: float
        self.FloorPrice: float
        self.HighestPrice: float
        self.LowestPrice: float
        self.MatchPrice: float
        self.PriceChange: float
        self.PercentPriceChange: float
        self.MatchVolume: int
        self.MatchValue: float
        self.TotalMatchValue: float
        self.TotalBuyTradeVolume: int
        self.TotalSellTradeVolume: int
        self.DealPrice: float
        self.TotalDealVolume: int
        self.TotalDealValue: float
        self.ForeignBuyVolumeTotal: int
        self.ForeignBuyValueTotal: float
        self.ForeignSellVolumeTotal: int
        self.ForeignSellValueTotal: float
        self.ForeignTotalRoom: int
        self.ForeignCurrentRoom: int

    def to_dataFrame(self) -> pd.DataFrame:
        ...

class HistoricalReturnData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.__private_attribute: pd.DataFrame = data
        self.Open: float
        self.Close: float
        self.Low: float
        self.High: float
        self.Volume: int
        self.Timestamp: str


    def to_dataFrame(self) -> pd.DataFrame:
        ...

class FiinDataHistorical:
    def __init__(self, access_token: str, ticker: str, from_date, to_date, multiplier: int = 1, timespan: str = 'minute', limit: int = 1000) -> None:
        self.ticker: str 
        self.from_date: str
        self.to_date: str 
        self.multiplier: int
        self.timespan: str
        self.limit: int 
        self.access_token: str 
        self.urlGetDataStock: str
        self.data: pd.DataFrame 

    def _fetch_historical_data(self) -> pd.DataFrame:
        ...

    def _preprocess_data(self) -> None:
        ...
    def _round_time(self, dt, start_time) -> str:
        ...
    def _group_by_data(self) -> pd.DataFrame:
        ...
    def _format_data(self) -> pd.DataFrame:
        ...
    def get_data(self) -> HistoricalReturnData:
        ...

class SubscribeForRealTime:
    def __init__(self, access_token: str, ticker: str, callback: callable) -> None:
        self.ticker: str
        self.url: str
        self.access_token: str
        self.urlGetDataStock: str
        self.data: pd.DataFrame
        self.connected: bool
        self.callback: callable
        self.hub_connection: self._build_connection
        self.return_data: RealTimeReturnData

    def _data_handler(self, message) -> None:
        ...
    def _build_connection(self) -> _build_connection:
        ...
    def _receive_message(self, message) -> None:
        ...
    def _handle_error(self, error) -> None:
        ...
    def _on_connect(self) -> None:
        ...
    def _on_disconnect(self) -> None:
        ...
    def _join_groups(self) -> None:
        ...
    def _run(self) -> None:
        ...
    def start(self) -> None:
        ...
    def stop(self) -> None:
        ...

class FiinIndicator:
    def ema(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def sma(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def rsi(self, col: pd.Series, window: int ) -> pd.Series:
        ...
    def macd(self, col: pd.Series, window_fast: int , window_slow: int , window_signal: int ) -> pd.Series:
        ...
    def macd_signal(self, col: pd.Series, window_fast: int , window_slow: int , window_signal: int ) -> pd.Series:
        ...
    def macd_diff(self, col: pd.Series, window_fast: int, window_slow: int , window_signal: int ) -> pd.Series:
        ...
    def bollinger_std(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def bollinger_mavg(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def bollinger_hband(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def bollinger_lband(self, col: pd.Series, window: int) -> pd.Series:
        ...
    def stoch(self, col: pd.Series, window: int, window_d: int) -> pd.Series:
        ...
    def stoch_signal(self, col: pd.Series, window: int, window_d: int) -> pd.Series:
        ...

class FiinSession:
    def __init__(self, username: str, password: str) -> None:
        self.username: str
        self.password: str
        self.access_token: str
        self.expired_token: str
        self.urlGetToken: str
        self.bodyGetToken: dict
        self.is_login: bool

    def _login(self) -> None:
        ...

    def _is_expired_token(self) -> bool:
        ...

    def _get_access_token(self) -> str:
        ...

    def FiinDataHistorical(self,ticker: str, from_date: str, 
                 to_date: str, 
                 multiplier: int , 
                 timespan: str, 
                 limit: int) -> FiinDataHistorical:
        ...

    def FiinIndicator(self) -> FiinIndicator:
        ...

    def SubscribeForRealTime(self, ticker: str, callback: callable) -> SubscribeForRealTime:
        ...
