import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.post("/bs/", json={"text": text})
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
    }


def test_get_stats_normalize():
    response = client.post("/bs/", json={"text": text, "normalize": True})
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
    response = client.post("/bs/", json={"text": text, "stat": "foo"})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "stat, expected",
    [
        ("c_letters", {"1": 1, "3": 2, "5": 2, "6": 2, "7": 2, "8": 1, "10": 1}),
        ("c_syllables", {"0": 1, "1": 2, "2": 4, "3": 3, "5": 1}),
        ("n_chars", 73),
        ("n_complex_words", 1),
        ("n_letters", 61),
        ("n_long_words", 6),
        ("n_monosyllable_words", 2),
        ("n_polysyllable_words", 8),
        ("n_simple_words", 9),
        ("n_spaces", 10),
        ("n_syllables", 24),
        ("n_unique_words", 11),
        ("n_words", 11),
        ("n_punctuations", 2),
        ("p_unique_words", pytest.approx(1.0, rel=0.1)),
        ("p_long_words", pytest.approx(0.55, rel=0.1)),
        ("p_complex_words", pytest.approx(0.1, rel=0.1)),
        ("p_simple_words", pytest.approx(0.8, rel=0.1)),
        ("p_monosyllable_words", pytest.approx(0.2, rel=0.1)),
        ("p_polysyllable_words", pytest.approx(0.7, rel=0.1)),
        ("p_letters", pytest.approx(0.8, rel=0.1)),
        ("p_spaces", pytest.approx(0.15, rel=0.1)),
        ("p_punctuations", pytest.approx(0.027, rel=0.1)),
    ],
)
def test_get_stat(stat, expected):
    response = client.post("/bs/", json={"text": text, "normalize": True, "stat": stat})
    assert response.status_code == 200
    assert response.json() == expected
