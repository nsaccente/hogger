from hogger.entities import RandomStat


def test_to_sql():
    # Given:
    outer_args = {
        "RandomProperty": "RandomProperty",
        "RandomSuffix": "RandomSuffix",
    }
    inner_args = {
        "model_field": "randomStat",
        "model_dict": {
            "randomStat": RandomStat(
                id=100,
                withSuffix=False,
            )
        },
        "cursor": None,
        "field_type": RandomStat,
    }

    # When:
    sql = RandomStat.to_sql(**outer_args)(**inner_args)

    # Then:
    assert sql["RandomProperty"] == 100
    assert sql["RandomSuffix"] == 0
    