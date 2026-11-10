from src.lambdas.clean.handler import clean_rows


def test_removes_duplicates():
    rows = [
        {"Order ID": "1", "Amount": "10"},
        {"Order ID": "1", "Amount": "10"},
    ]
    assert len(clean_rows(rows)) == 1


def test_drops_missing_amount():
    rows = [{"Order ID": "2", "Amount": ""}]
    assert clean_rows(rows) == []


def test_drops_invalid_and_negative_amounts():
    rows = [
        {"Order ID": "3", "Amount": "abc"},
        {"Order ID": "4", "Amount": "-5"},
    ]
    assert clean_rows(rows) == []


def test_standardizes_columns_and_converts_amount():
    rows = [{"Order ID": "5", "Amount": "20"}]
    assert clean_rows(rows) == [{"order_id": "5", "amount": 20.0}]