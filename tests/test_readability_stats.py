import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.post("/rs/", json={"text": text})
    assert response.status_code == 200
    assert response.json() == {
        "flesch_kincaid_grade": 4.727272727272727,
        "flesch_reading_easy": 61.40772727272727,
        "coleman_liau_index": 6.7600454545454625,
        "smog_index": 8.891153770860452,
        "automated_readability_index": 6.7600454545454625,
        "lix": 65.54545454545455,
    }


def test_get_stat_error():
    response = client.post("/rs/", json={"text": text, "stat": "foo"})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "stat, expected",
    [
        ("flesch_kincaid_grade", pytest.approx(4.7, rel=0.1)),
        ("flesch_reading_easy", pytest.approx(61.4, rel=0.1)),
        ("coleman_liau_index", pytest.approx(6.7, rel=0.1)),
        ("smog_index", pytest.approx(8.9, rel=0.1)),
        ("automated_readability_index", pytest.approx(6.7, rel=0.1)),
        ("lix", pytest.approx(65.5, rel=0.1)),
    ],
)
def test_get_stat(stat, expected):
    response = client.post("/rs/", json={"text": text, "stat": stat})
    assert response.status_code == 200
    assert response.json() == expected
