import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.get("/bs/", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {
        "c_letters": {"1": 1, "3": 2, "5": 2, "6": 2, "7": 2, "8": 1, "10": 1},
        "c_syllables": {"0": 1, "1": 2, "2": 4, "3": 3, "5": 1},
        "n_sents": 1,
        "n_words": 11,
        "n_unique_words": 11,
        "n_long_words": 6,
        "n_complex_words": 1,
        "n_simple_words": 9,
        "n_monosyllable_words": 2,
        "n_polysyllable_words": 8,
        "n_chars": 73,
        "n_letters": 61,
        "n_spaces": 10,
        "n_syllables": 24,
        "n_punctuations": 2,
        "p_complex_words": 0.09090909090909091,
        "p_letters": 0.8356164383561644,
        "p_long_words": 0.5454545454545454,
        "p_monosyllable_words": 0.18181818181818182,
        "p_polysyllable_words": 0.7272727272727273,
        "p_punctuations": 0.0273972602739726,
        "p_simple_words": 0.8181818181818182,
        "p_spaces": 0.136986301369863,
        "p_unique_words": 1.0,
    }


def test_get_stat_error():
    response = client.get("/bs/foo", params={"text": text})
    assert response.status_code == 404


def test_c_letters():
    response = client.get("/bs/c_letters", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"1": 1, "3": 2, "5": 2, "6": 2, "7": 2, "8": 1, "10": 1}


def test_c_syllables():
    response = client.get("/bs/c_syllables", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"0": 1, "1": 2, "2": 4, "3": 3, "5": 1}


def test_n_chars():
    response = client.get("/bs/n_chars", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 73


def test_n_complex_words():
    response = client.get("/bs/n_complex_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 1


def test_n_letters():
    response = client.get("/bs/n_letters", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 61


def test_n_long_words():
    response = client.get("/bs/n_long_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 6


def test_n_monosyllable_words():
    response = client.get("/bs/n_monosyllable_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 2


def test_n_polysyllable_words():
    response = client.get("/bs/n_polysyllable_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 8


def test_n_sents():
    response = client.get("/bs/n_sents", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 1


def test_n_simple_words():
    response = client.get("/bs/n_simple_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 9


def test_n_spaces():
    response = client.get("/bs/n_spaces", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 10


def test_n_syllables():
    response = client.get("/bs/n_syllables", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 24


def test_n_unique_words():
    response = client.get("/bs/n_unique_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 11


def test_n_words():
    response = client.get("/bs/n_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 11


def test_n_punctuations():
    response = client.get("/bs/n_punctuations", params={"text": text})
    assert response.status_code == 200
    assert response.json() == 2


def test_p_unique_words():
    response = client.get("/bs/p_unique_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(1.0, rel=0.1)


def test_p_long_words():
    response = client.get("/bs/p_long_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.55, rel=0.1)


def test_p_complex_words():
    response = client.get("/bs/p_complex_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.1, rel=0.1)


def test_p_simple_words():
    response = client.get("/bs/p_simple_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.8, rel=0.1)


def test_p_monosyllable_words():
    response = client.get("/bs/p_monosyllable_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.2, rel=0.1)


def test_p_polysyllable_words():
    response = client.get("/bs/p_polysyllable_words", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.7, rel=0.1)


def test_p_letters():
    response = client.get("/bs/p_letters", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.8, rel=0.1)


def test_p_spaces():
    response = client.get("/bs/p_spaces", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.15, rel=0.1)


def test_p_punctuations():
    response = client.get("/bs/p_punctuations", params={"text": text})
    assert response.status_code == 200
    assert response.json() == pytest.approx(0.027, rel=0.1)
