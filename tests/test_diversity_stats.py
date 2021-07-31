import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.get("/ds/", params={"text": text})
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
    response = client.get("/ds/foo", params={"text": text})
    assert response.status_code == 404


def test_ttr():
    response = client.get("/ds/ttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_rttr():
    response = client.get("/ds/rttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(3.3, rel=0.1)


def test_cttr():
    response = client.get("/ds/cttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(2.3, rel=0.1)


def test_httr():
    response = client.get("/ds/httr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_sttr():
    response = client.get("/ds/sttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_mttr():
    response = client.get("/ds/mttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.0, rel=0.1)


def test_dttr():
    response = client.get("/ds/dttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.0, rel=0.1)


def test_mattr():
    response = client.get("/ds/mattr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_msttr():
    response = client.get("/ds/msttr", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_mtld():
    response = client.get("/ds/mtld", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.0, rel=0.1)


def test_mamtld():
    response = client.get("/ds/mamtld", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_hdd():
    response = client.get("/ds/hdd", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(-1.0, rel=0.1)


def test_simpson_index():
    response = client.get("/ds/simpson_index", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.0, rel=0.1)


def test_hapax_index():
    response = client.get("/ds/hapax_index", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.0, rel=0.1)
