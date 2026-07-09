from src.etl.normaliser import normalize_year


def test_year_1():
    assert normalize_year(2024) == "2024"


def test_year_2():
    assert normalize_year("2023") == "2023"


def test_year_3():
    assert normalize_year("2022-23") == "2022"


def test_year_4():
    assert normalize_year("2021-2022") == "2021"


def test_year_5():
    assert normalize_year(None) is None


def test_year_6():
    assert normalize_year(" 2020 ") == "2020"


def test_year_7():
    assert normalize_year("2019-20") == "2019"


def test_year_8():
    assert normalize_year("2018") == "2018"


def test_year_9():
    assert normalize_year("2017-2018") == "2017"


def test_year_10():
    assert normalize_year(2016) == "2016"


def test_year_11():
    assert normalize_year("2015") == "2015"


def test_year_12():
    assert normalize_year("2014-15") == "2014"


def test_year_13():
    assert normalize_year("2013") == "2013"


def test_year_14():
    assert normalize_year("2012") == "2012"


def test_year_15():
    assert normalize_year("2011-2012") == "2011"


def test_year_16():
    assert normalize_year("2010") == "2010"


def test_year_17():
    assert normalize_year("2009") == "2009"


def test_year_18():
    assert normalize_year("2008-09") == "2008"


def test_year_19():
    assert normalize_year("2007") == "2007"


def test_year_20():
    assert normalize_year("2006") == "2006"