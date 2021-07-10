import sys

from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.get("/ms/?text=" + text)
    assert response.status_code == 200
    assert response.json() == {
        "pos": {"VERB": 2, "ADVB": 2, "ADJF": 2, "NPRO": 1, "NOUN": 3, "PREP": 1},
        "animacy": {"null": 8, "inan": 3},
        "aspect": {"impf": 2, "null": 9},
        "case": {"null": 5, "nomn": 2, "accs": 1, "loct": 1, "gent": 2},
        "gender": {"null": 5, "masc": 3, "femn": 1, "neut": 2},
        "involvement": {"null": 11},
        "mood": {"indc": 2, "null": 9},
        "number": {"sing": 8, "null": 3},
        "person": {"3per": 2, "null": 9},
        "tense": {"pres": 2, "null": 9},
        "transitivity": {"intr": 1, "null": 9, "tran": 1},
        "voice": {"null": 11},
    }


def test_get_stat_error():
    response = client.get("/ms/foo?text=" + text)
    assert response.status_code == 404


def test_pos():
    response = client.get("/ms/pos?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"VERB": 2, "ADVB": 2, "ADJF": 2, "NPRO": 1, "NOUN": 3, "PREP": 1}


def test_animacy():
    response = client.get("/ms/animacy?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"null": 8, "inan": 3}


def test_aspect():
    response = client.get("/ms/aspect?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"impf": 2, "null": 9}


def test_case():
    response = client.get("/ms/case?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"null": 5, "nomn": 2, "accs": 1, "loct": 1, "gent": 2}


def test_gender():
    response = client.get("/ms/gender?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"null": 5, "masc": 3, "femn": 1, "neut": 2}


def test_involvement():
    response = client.get("/ms/involvement?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"null": 11}


def test_mood():
    response = client.get("/ms/mood?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"indc": 2, "null": 9}


def test_number():
    response = client.get("/ms/number?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"sing": 8, "null": 3}


def test_person():
    response = client.get("/ms/person?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"3per": 2, "null": 9}


def test_tense():
    response = client.get("/ms/tense?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"pres": 2, "null": 9}


def test_transitivity():
    response = client.get("/ms/transitivity?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"intr": 1, "null": 9, "tran": 1}


def test_voice():
    response = client.get("/ms/voice?text=" + text)
    assert response.status_code == 200
    assert response.json() == {"null": 11}


def test_explain_text():
    response = client.get("/ms/explain?stats=pos&stats=tense", params={"text": text})
    assert response.status_code == 200
    assert response.json() == [
        ["Живет", {"pos": "VERB", "tense": "pres"}],
        ["свободно", {"pos": "ADVB", "tense": None}],
        ["только", {"pos": "ADVB", "tense": None}],
        ["тот", {"pos": "ADJF", "tense": None}],
        ["кто", {"pos": "NPRO", "tense": None}],
        ["находит", {"pos": "VERB", "tense": "pres"}],
        ["радость", {"pos": "NOUN", "tense": None}],
        ["в", {"pos": "PREP", "tense": None}],
        ["исполнении", {"pos": "NOUN", "tense": None}],
        ["своего", {"pos": "ADJF", "tense": None}],
        ["долга", {"pos": "NOUN", "tense": None}],
    ]


def test_explain_text_error():
    response = client.get("/ms/explain", params={"text": text, "stats": "foo"})
    assert response.status_code == 404
