from hogger.types import Duration


def test_from_milli():
    ms_in_day = 86400000
    ms_in_hour = 3600000
    ms_in_min = 60000
    ms_in_sec = 1000
    d = Duration.from_milli(ms_in_day)