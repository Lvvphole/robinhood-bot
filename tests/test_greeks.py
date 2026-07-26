from zero_dte_bot.greeks import black_scholes_greeks


def test_atm_call_greeks_are_sensible() -> None:
    result = black_scholes_greeks(
        spot=100.0,
        strike=100.0,
        time_years=30 / 365,
        rate=0.05,
        volatility=0.20,
        right="C",
    )
    assert 0.45 < result.delta < 0.65
    assert result.gamma > 0
    assert result.theta_per_day < 0
    assert result.vega_per_vol_point > 0


def test_put_delta_is_negative() -> None:
    result = black_scholes_greeks(
        spot=100.0,
        strike=100.0,
        time_years=1 / 365,
        rate=0.05,
        volatility=0.25,
        right="P",
    )
    assert -1.0 < result.delta < 0.0
