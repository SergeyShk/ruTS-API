import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.get("/rs/?text=" + text)
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
    response = client.get("/rs/foo?text=" + text)
    assert response.status_code == 404


def test_flesch_kincaid_grade():
    response = client.get("/rs/flesch_kincaid_grade?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(4.7, rel=0.1)


def test_flesch_reading_easy():
    response = client.get("/rs/flesch_reading_easy?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(61.4, rel=0.1)


def test_coleman_liau_index():
    response = client.get("/rs/coleman_liau_index?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(6.7, rel=0.1)


def test_smog_index():
    response = client.get("/rs/smog_index?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(8.9, rel=0.1)


def test_automated_readability_index():
    response = client.get("/rs/automated_readability_index?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(6.7, rel=0.1)


def test_lix():
    response = client.get("/rs/lix?text=" + text)
    assert response.status_code == 200
    assert response.json() == pytest.approx(65.5, rel=0.1)
