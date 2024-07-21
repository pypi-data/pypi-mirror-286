from pious.range import Range


def test_range_constructor():
    r = Range("AA")
    assert r["AhAd"] == 1.0
    assert r["AhAc"] == 1.0
    assert r["AhAs"] == 1.0
    assert r["AdAh"] == 1.0
    assert r["AdAc"] == 1.0
    assert r["AdAs"] == 1.0
