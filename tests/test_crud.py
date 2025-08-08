import pytest
import requests
from db import clear_db


@pytest.fixture(scope="session", autouse=True)
def clear_database_before_tests():
    clear_db()


def test_with_zero_transactions():
    response = requests.get(url="http://127.0.0.1:8000/transactions")
    assert response.status_code == 200
    assert response.json() == []


valid_data = [
    ({"value": 123.45, "dataHora": "2025-08-03T12:34:56.789-03:00"}),
    ({"value": 1.1, "dataHora": "1990-08-03T12:34:56.789-03:00"}),
]


@pytest.mark.parametrize("t", valid_data)
def test_with_some_valid_transactions(t):
    response = requests.post(url="http://127.0.0.1:8000/transactions", json=t)
    assert response.status_code == 201
    assert response.json() == {"message": "Transaction added successfully!"}


invalid_data = [
    (
        {"value": -123.45, "dataHora": "2025-08-03T12:34:56.789-03:00"},
        {"detail": "value can`t be negative!"},
    ),
    (
        {"value": 1.1, "dataHora": "2990-08-03T12:34:56.789-03:00"},
        {"detail": "dataHora can`t be in the future!"},
    ),
]


@pytest.mark.parametrize("t,message", invalid_data)
def test_with_some_invalid_transactions(t, message):
    response = requests.post(url="http://127.0.0.1:8000/transactions", json=t)
    assert response.status_code == 400
    assert response.json() == message


def test_deleting_ransactions():
    response = requests.get(url="http://127.0.0.1:8000/transactions")
    _first_id = response.json()[1]["id"]
    response = requests.delete(url=f"http://127.0.0.1:8000/transactions/{_first_id}")
    assert response.status_code == 202
    assert response.json() == {"message": "Transaction deleted successfully!"}
    response = requests.get(url="http://127.0.0.1:8000/transactions")
    for r in response.json():
        if r["id"] == _first_id:
            assert False
    assert True
