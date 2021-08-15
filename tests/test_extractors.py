import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)

text_sents = (
    "Да. Времена изменились. Дети больше не слушаются своих родителей, и каждый пишет книги."
)

text_words = "Лучшее время, чтобы посадить дерево, было 20 лет назад."


class TestSentsExtractor(object):
    def test_extract(self):
        response = client.post("/extract/sents", json={"text": text_sents})
        assert response.status_code == 200
        assert response.json() == [
            "Да.",
            "Времена изменились.",
            "Дети больше не слушаются своих родителей, и каждый пишет книги.",
        ]

    @pytest.mark.parametrize(
        "min_len, expected",
        [
            (5, 2),
            (50, 1),
        ],
    )
    def test_extract_min_len(self, min_len, expected):
        response = client.post("/extract/sents", json={"text": text_sents, "min_len": min_len})
        assert response.status_code == 200
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "max_len, expected",
        [
            (5, 1),
            (50, 2),
        ],
    )
    def test_extract_max_len(self, max_len, expected):
        response = client.post("/extract/sents", json={"text": text_sents, "max_len": max_len})
        assert response.status_code == 200
        assert len(response.json()) == expected


class TestWordsExtractor(object):
    def test_extract(self):
        response = client.post("/extract/words", json={"text": text_words})
        assert response.status_code == 200
        assert response.json() == [
            "Лучшее",
            "время",
            "чтобы",
            "посадить",
            "дерево",
            "было",
            "20",
            "лет",
            "назад",
        ]

    @pytest.mark.parametrize(
        "filter_punct, expected",
        [
            (True, 9),
            (False, 12),
        ],
    )
    def test_extract_filter_punct(self, filter_punct, expected):
        response = client.post(
            "/extract/words", json={"text": text_words, "filter_punct": filter_punct}
        )
        assert response.status_code == 200
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "filter_nums, expected",
        [
            (True, 8),
            (False, 9),
        ],
    )
    def test_extract_filter_nums(self, filter_nums, expected):
        response = client.post(
            "/extract/words", json={"text": text_words, "filter_nums": filter_nums}
        )
        assert response.status_code == 200
        assert len(response.json()) == expected

    def test_extract_use_lexemes(self):
        response = client.post("/extract/words", json={"text": text_words, "use_lexemes": True})
        assert response.status_code == 200
        assert response.json() == [
            "хороший",
            "время",
            "чтобы",
            "посадить",
            "дерево",
            "быть",
            "20",
            "год",
            "назад",
        ]

    def test_extract_stopwords(self):
        response = client.post(
            "/extract/words", json={"text": text_words, "stopwords": ["чтобы", "год"]}
        )
        assert response.status_code == 200
        assert response.json() == [
            "Лучшее",
            "время",
            "посадить",
            "дерево",
            "было",
            "20",
            "лет",
            "назад",
        ]

    def test_extract_lowercase(self):
        response = client.post("/extract/words", json={"text": text_words, "lowercase": True})
        assert response.status_code == 200
        assert response.json() == [
            "лучшее",
            "время",
            "чтобы",
            "посадить",
            "дерево",
            "было",
            "20",
            "лет",
            "назад",
        ]

    def test_extract_ngram_range(self):
        response = client.post("/extract/words", json={"text": text_words, "ngram_range": (3, 3)})
        assert response.status_code == 200
        assert response.json() == [
            "Лучшее_время_чтобы",
            "время_чтобы_посадить",
            "чтобы_посадить_дерево",
            "посадить_дерево_было",
            "дерево_было_20",
            "было_20_лет",
            "20_лет_назад",
        ]

    @pytest.mark.parametrize(
        "most_common, expected",
        [
            (3, 3),
            (6, 6),
        ],
    )
    def test_extract_most_common(self, most_common, expected):
        response = client.post(
            "/extract/words", json={"text": text_words, "most_common": most_common}
        )
        assert response.status_code == 200
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "min_len, expected",
        [
            (5, 6),
            (8, 1),
        ],
    )
    def test_extract_min_len(self, min_len, expected):
        response = client.post("/extract/words", json={"text": text_words, "min_len": min_len})
        assert response.status_code == 200
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "max_len, expected",
        [
            (6, 8),
            (3, 2),
        ],
    )
    def test_extract_max_len(self, max_len, expected):
        response = client.post("/extract/words", json={"text": text_words, "max_len": max_len})
        assert response.status_code == 200
        assert len(response.json()) == expected
