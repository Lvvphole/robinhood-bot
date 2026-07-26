from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class OptionRight(str, Enum):
    CALL = "C"
    PUT = "P"


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class OptionQuote:
    timestamp: datetime
    expiration: date
    strike: float
    right: OptionRight
    bid: float
    ask: float
    last: float
    volume: int
    open_interest: int
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    symbol: str = ""

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2.0

    @property
    def spread(self) -> float:
        return max(0.0, self.ask - self.bid)

    @property
    def spread_fraction(self) -> float:
        return self.spread / self.mid if self.mid > 0 else float("inf")


@dataclass(slots=True)
class Position:
    quote: OptionQuote
    quantity: int
    entry_time: datetime
    entry_price: float
    highest_mark: float
    direction: int


@dataclass(frozen=True, slots=True)
class Trade:
    symbol: str
    right: OptionRight
    strike: float
    expiration: date
    quantity: int
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    gross_pnl: float
    fees: float
    net_pnl: float
    exit_reason: str
    entry_delta: float
    entry_gamma: float
    entry_theta: float
    entry_vega: float
