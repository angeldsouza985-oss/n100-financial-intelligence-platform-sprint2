from src.etl.normaliser import normalize_ticker


def test_ticker_1():
    assert normalize_ticker("tcs.ns") == "TCS"


def test_ticker_2():
    assert normalize_ticker("infy") == "INFY"


def test_ticker_3():
    assert normalize_ticker("reliance.bo") == "RELIANCE"


def test_ticker_4():
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"


def test_ticker_5():
    assert normalize_ticker(None) is None


def test_ticker_6():
    assert normalize_ticker("itc") == "ITC"


def test_ticker_7():
    assert normalize_ticker("asianpaint.ns") == "ASIANPAINT"


def test_ticker_8():
    assert normalize_ticker("sbin") == "SBIN"


def test_ticker_9():
    assert normalize_ticker("lt.bo") == "LT"


def test_ticker_10():
    assert normalize_ticker("maruti") == "MARUTI"


def test_ticker_11():
    assert normalize_ticker("ongc") == "ONGC"


def test_ticker_12():
    assert normalize_ticker("titan.ns") == "TITAN"


def test_ticker_13():
    assert normalize_ticker("nestleind") == "NESTLEIND"


def test_ticker_14():
    assert normalize_ticker("wipro") == "WIPRO"


def test_ticker_15():
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"