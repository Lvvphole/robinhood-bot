from __future__ import annotations

from collections.abc import Callable
from typing import Any


class RobinhoodAgentGateway:
    """Adapter contract for the uploaded Robinhood Agentic tool surface.

    The local package does not possess brokerage credentials or direct tool access.
    Supply a trusted executor that maps the documented tool names to authenticated
    calls. Live placement remains disabled by configuration in v0.1.
    """

    def __init__(self, executor: Callable[[str, dict[str, Any]], dict[str, Any]]):
        self._execute = executor

    def get_option_chain(self, underlying: str, expiration: str) -> dict:
        return self._execute(
            "get_option_chains", {"underlying": underlying, "expiration": expiration}
        )

    def get_option_quotes(self, contract_ids: list[str]) -> dict:
        return self._execute("get_option_quotes", {"contract_ids": contract_ids})

    def review_option_order(self, order: dict) -> dict:
        return self._execute("review_option_order", order)

    def place_option_order(self, reviewed_order: dict) -> dict:
        raise RuntimeError("Live order placement is disabled in version 0.1.")

    def cancel_option_order(self, order_id: str) -> dict:
        return self._execute("cancel_option_order", {"order_id": order_id})
