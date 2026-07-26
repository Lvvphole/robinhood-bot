from __future__ import annotations

from .models import OptionQuote


class FillModel:
    """Conservative bid/ask execution model for research."""

    def __init__(self, config: dict):
        self.slippage_fraction = float(config["slippage_fraction_of_spread"])
        self.minimum_slippage = float(config["minimum_slippage"])

    def buy_price(self, quote: OptionQuote) -> float:
        slippage = max(self.minimum_slippage, quote.spread * self.slippage_fraction)
        return round(quote.ask + slippage, 4)

    def sell_price(self, quote: OptionQuote) -> float:
        slippage = max(self.minimum_slippage, quote.spread * self.slippage_fraction)
        return round(max(0.0, quote.bid - slippage), 4)
