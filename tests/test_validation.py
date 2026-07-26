from zero_dte_bot.validation import validate_numeric_invariants


def test_floating_point_drift_is_accepted() -> None:
    assert validate_numeric_invariants(
        baseline=0.0,
        target=-0.2,
        current=-0.20000000000000004,
        gap=-0.2,
        progress_delta=-0.20000000000000004,
    )


def test_material_drift_is_rejected() -> None:
    assert not validate_numeric_invariants(
        baseline=0.0,
        target=-0.2,
        current=-0.20001,
        gap=-0.2,
        progress_delta=-0.2,
    )
