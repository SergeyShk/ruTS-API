import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text = "Времена изменились. Дети больше не слушаются своих родителей, и каждый пишет книги."


def test_extract_sents():
    response = client.get("/extract/sents/", params={"text": text})
    assert response.status_code == 200
    assert response.json() == [
        "Времена изменились.",
        "Дети больше не слушаются своих родителей, и каждый пишет книги.",
    ]


def test_extract_words():
    response = client.get("/extract/words/", params={"text": text})
    assert response.status_code == 200
    assert response.json() == [
        "Времена",
        "изменились",
        "Дети",
        "больше",
        "не",
        "слушаются",
        "своих",
        "родителей",
        "и",
        "каждый",
        "пишет",
        "книги",
    ]
