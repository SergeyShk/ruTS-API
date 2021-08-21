import sys

from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Живет свободно только тот, кто находит радость в исполнении своего долга."


def test_get_stats():
    response = client.post("/ms/", json={"text": text})
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


def test_get_stats_filter_none():
    response = client.post("/ms/", json={"text": text, "filter_none": True})
    assert response.status_code == 200
    assert response.json() == {
        "pos": {"VERB": 2, "ADVB": 2, "ADJF": 2, "NPRO": 1, "NOUN": 3, "PREP": 1},
        "animacy": {"inan": 3},
        "aspect": {"impf": 2},
        "case": {"nomn": 2, "accs": 1, "loct": 1, "gent": 2},
        "gender": {"masc": 3, "femn": 1, "neut": 2},
        "involvement": {},
        "mood": {"indc": 2},
        "number": {"sing": 8},
        "person": {"3per": 2},
        "tense": {"pres": 2},
        "transitivity": {"intr": 1, "tran": 1},
        "voice": {},
    }


def test_get_stats_error():
    response = client.post("/ms/", json={"text": text, "stats": ("foo",)})
    assert response.status_code == 404


def test_pos():
    response = client.post("/ms/", json={"text": text, "stats": ("pos",)})
    assert response.status_code == 200
    assert response.json() == {"VERB": 2, "ADVB": 2, "ADJF": 2, "NPRO": 1, "NOUN": 3, "PREP": 1}


def test_animacy():
    response = client.post("/ms/", json={"text": text, "stats": ("animacy",)})
    assert response.status_code == 200
    assert response.json() == {"null": 8, "inan": 3}


def test_aspect():
    response = client.post("/ms/", json={"text": text, "stats": ("aspect",)})
    assert response.status_code == 200
    assert response.json() == {"impf": 2, "null": 9}


def test_case():
    response = client.post("/ms/", json={"text": text, "stats": ("case",)})
    assert response.status_code == 200
    assert response.json() == {"null": 5, "nomn": 2, "accs": 1, "loct": 1, "gent": 2}


def test_gender():
    response = client.post("/ms/", json={"text": text, "stats": ("gender",)})
    assert response.status_code == 200
    assert response.json() == {"null": 5, "masc": 3, "femn": 1, "neut": 2}


def test_involvement():
    response = client.post("/ms/", json={"text": text, "stats": ("involvement",)})
    assert response.status_code == 200
    assert response.json() == {"null": 11}


def test_mood():
    response = client.post("/ms/", json={"text": text, "stats": ("mood",)})
    assert response.status_code == 200
    assert response.json() == {"indc": 2, "null": 9}


def test_number():
    response = client.post("/ms/", json={"text": text, "stats": ("number",)})
    assert response.status_code == 200
    assert response.json() == {"sing": 8, "null": 3}


def test_person():
    response = client.post("/ms/", json={"text": text, "stats": ("person",)})
    assert response.status_code == 200
    assert response.json() == {"3per": 2, "null": 9}


def test_tense():
    response = client.post("/ms/", json={"text": text, "stats": ("tense",)})
    assert response.status_code == 200
    assert response.json() == {"pres": 2, "null": 9}


def test_transitivity():
    response = client.post("/ms/", json={"text": text, "stats": ("transitivity",)})
    assert response.status_code == 200
    assert response.json() == {"intr": 1, "null": 9, "tran": 1}


def test_voice():
    response = client.post("/ms/", json={"text": text, "stats": ("voice",)})
    assert response.status_code == 200
    assert response.json() == {"null": 11}


def test_explain_text():
    response = client.post("/ms/explain", json={"text": text, "stats": ("pos", "tense")})
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
    response = client.post("/ms/explain", json={"text": text, "stats": ("foo",)})
    assert response.status_code == 404
