from __future__ import annotations

from typing import Protocol


class BrokerGateway(Protocol):
    """Minimal live/paper broker boundary. Implementations must review before place."""

    def get_option_chain(self, underlying: str, expiration: str) -> dict: ...

    def get_option_quotes(self, contract_ids: list[str]) -> dict: ...

    def review_option_order(self, order: dict) -> dict: ...

    def place_option_order(self, reviewed_order: dict) -> dict: ...

    def cancel_option_order(self, order_id: str) -> dict: ...
