from hogger.types import Duration


def test_from_milli():
    # Number of ms in a day, hour, min, sec
    d = 86400000
    h = 3600000
    m = 60000
    s = 1000

    a = Duration.from_milli(2 * d + 3 * h + 5 * m + 22 * s + 250)
    assert a.days == 2
    assert a.hours == 3
    assert a.minutes == 5
    assert a.seconds == 22
    assert a.milli == 250

    # test time rollover.
    b = Duration.from_milli(25 * h + 61 * m + 61 * s + 1001)
    assert b.days == 1
    assert b.hours == 2
    assert b.minutes == 2
    assert b.seconds == 2
    assert b.milli == 1


def test_from_seconds():
    # Number of s in a day, hour, min
    d = 86400
    h = 3600
    m = 60

    a = Duration.from_seconds(2 * d + 3 * h + 5 * m + 22)
    assert a.days == 2
    assert a.hours == 3
    assert a.minutes == 5
    assert a.seconds == 22
    assert a.milli == 0
    print(a)
