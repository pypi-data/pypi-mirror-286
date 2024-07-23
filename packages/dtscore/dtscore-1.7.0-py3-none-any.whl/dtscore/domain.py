"""
    Domain classes

    These classes are independent of a particular implementation
"""
#   to postpone resolution of annotations. See @classmethod returning Quote below.
from __future__ import annotations

import datetime as dt


class Quote:
    def __init__(
            self, date:dt.datetime, close:float, high:float, low:float, open:float, volume:int,
            adjClose:float=None, adjHigh:float=None, adjLow:float=None, adjOpen:float=None, adjVolume:int=None,
            divCash:float=None, splitFactor:float=None
        ):
        self.date = date
        self.close = close,
        self.high = high,
        self.low = low,
        self.open = open,
        self.volume = volume,
        self.adjClose = adjClose,
        self.adjHigh = adjHigh,
        self.adjLow = adjLow,
        self.adjOpen = adjOpen,
        self.adjVolume = adjVolume,
        self.divCash = divCash,
        self.splitFactor = splitFactor

    def __str__(self) -> str:
        return f"Quote[date={self.date}, close={self.close}, high={self.high}, low={self.low}, open={self.open}, volume={self.volume} \
            adjClose={self.adjClose}, adjHigh={self.adjHigh}, adjLow={self.adjLow}, adjOpen={self.adjOpen}, adjVolume={self.adjVolume}, \
            divCash={self.divCash}, splitFactor={self.splitFactor}"
