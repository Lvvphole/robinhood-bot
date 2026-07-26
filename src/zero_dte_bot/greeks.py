from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt

from scipy.stats import norm


@dataclass(frozen=True, slots=True)
class Greeks:
    price: float
    delta: float
    gamma: float
    theta_per_day: float
    vega_per_vol_point: float
    rho_per_rate_point: float


def black_scholes_greeks(
    *,
    spot: float,
    strike: float,
    time_years: float,
    rate: float,
    volatility: float,
    right: str,
    dividend_yield: float = 0.0,
) -> Greeks:
    """Return European Black-Scholes values.

    For 0DTE screening this is a fallback only. Historical exchange/broker Greeks
    are preferred because discrete dividends, microstructure, and the volatility
    surface can materially affect near-expiry contracts.
    """
    if min(spot, strike, time_years, volatility) <= 0:
        raise ValueError("spot, strike, time_years, and volatility must be positive")
    if right not in {"C", "P"}:
        raise ValueError("right must be 'C' or 'P'")

    sqrt_t = sqrt(time_years)
    d1 = (
        log(spot / strike)
        + (rate - dividend_yield + 0.5 * volatility**2) * time_years
    ) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t
    discount_r = exp(-rate * time_years)
    discount_q = exp(-dividend_yield * time_years)
    density = exp(-0.5 * d1**2) / sqrt(2.0 * pi)

    gamma = discount_q * density / (spot * volatility * sqrt_t)
    vega = spot * discount_q * density * sqrt_t / 100.0

    if right == "C":
        price = spot * discount_q * norm.cdf(d1) - strike * discount_r * norm.cdf(d2)
        delta = discount_q * norm.cdf(d1)
        theta_year = (
            -(spot * discount_q * density * volatility) / (2.0 * sqrt_t)
            - rate * strike * discount_r * norm.cdf(d2)
            + dividend_yield * spot * discount_q * norm.cdf(d1)
        )
        rho = strike * time_years * discount_r * norm.cdf(d2) / 100.0
    else:
        price = strike * discount_r * norm.cdf(-d2) - spot * discount_q * norm.cdf(-d1)
        delta = discount_q * (norm.cdf(d1) - 1.0)
        theta_year = (
            -(spot * discount_q * density * volatility) / (2.0 * sqrt_t)
            + rate * strike * discount_r * norm.cdf(-d2)
            - dividend_yield * spot * discount_q * norm.cdf(-d1)
        )
        rho = -strike * time_years * discount_r * norm.cdf(-d2) / 100.0

    return Greeks(
        price=float(price),
        delta=float(delta),
        gamma=float(gamma),
        theta_per_day=float(theta_year / 365.0),
        vega_per_vol_point=float(vega),
        rho_per_rate_point=float(rho),
    )
