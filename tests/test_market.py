from analysis.market import format_change


def test_positive_change():

    result = format_change(2.5)

    assert result == "↑ 2.50%"


def test_negative_change():

    result = format_change(-2.5)

    assert result == "↓ 2.50%"


def test_zero_change():

    result = format_change(0)

    assert result == "→ 0.00%"


def test_none_change():

    result = format_change(None)

    assert result == "N/A"