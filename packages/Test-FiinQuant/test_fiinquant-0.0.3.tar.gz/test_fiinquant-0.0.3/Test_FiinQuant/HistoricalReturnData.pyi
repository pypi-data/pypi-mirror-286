import pandas as pd


class HistoricalReturnData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.__private_attribute: pd.DataFrame
        self.Open: float
        self.Close: float
        self.Low: float
        self.High: float
        self.Volume: int
        self.Timestamp: str

    def to_dataFrame(self) -> pd.DataFrame: ...

