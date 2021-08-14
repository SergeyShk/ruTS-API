import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.post("/ds/", json={"text": text})
    assert response.status_code == 200
    assert response.json() == {
        "ttr": 1,
        "rttr": 3.3166247903554,
        "cttr": 2.345207879911715,
        "httr": 1,
        "sttr": 1,
        "mttr": 0,
        "dttr": 0,
        "mattr": 1,
        "msttr": 1,
        "mtld": 0,
        "mamtld": 1,
        "hdd": -1,
        "simpson_index": 0,
        "hapax_index": 0,
    }


def test_get_stat_error():
    response = client.post("/bs/", json={"text": text, "stat": "foo"})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "stat, expected",
    [
        ("ttr", pytest.approx(1.0, rel=0.1)),
        ("rttr", pytest.approx(3.3, rel=0.1)),
        ("cttr", pytest.approx(2.3, rel=0.1)),
        ("httr", pytest.approx(1.0, rel=0.1)),
        ("sttr", pytest.approx(1.0, rel=0.1)),
        ("mttr", pytest.approx(0.0, rel=0.1)),
        ("dttr", pytest.approx(0.0, rel=0.1)),
        ("mattr", pytest.approx(1.0, rel=0.1)),
        ("msttr", pytest.approx(1.0, rel=0.1)),
        ("mtld", pytest.approx(0.0, rel=0.1)),
        ("mamtld", pytest.approx(1.0, rel=0.1)),
        ("hdd", pytest.approx(-1.0, rel=0.1)),
        ("simpson_index", pytest.approx(0.0, rel=0.1)),
        ("hapax_index", pytest.approx(0.0, rel=0.1)),
    ],
)
def test_get_stat(stat, expected):
    response = client.post("/ds/", json={"text": text, "stat": stat})
    assert response.status_code == 200
    assert response.json() == expected
