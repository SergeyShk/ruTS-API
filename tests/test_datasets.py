import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("..")
from api.main import api

client = TestClient(api)


class TestSovChLit:
    def test_get_texts(self):
        response = client.post("/datasets/scl", json={"limit": 2})
        assert response.status_code == 200
        for text in response.json():
            assert isinstance(text, str)

    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_get_texts_limit(self, limit):
        response = client.post("/datasets/scl", json={"limit": limit})
        assert response.status_code == 200
        assert sum(1 for _ in response.json()) == limit

    @pytest.mark.parametrize("min_len", [100, 200, 1000])
    def test_get_texts_min_len(self, min_len):
        response = client.post("/datasets/scl", json={"limit": 5, "min_len": min_len})
        assert response.status_code == 200
        assert all(len(text) >= min_len for text in response.json())

    @pytest.mark.parametrize("max_len", [250, 500, 1000])
    def test_get_texts_max_len(self, max_len):
        response = client.post("/datasets/scl", json={"limit": 5, "max_len": max_len})
        assert response.status_code == 200
        assert all(len(text) < max_len for text in response.json())

    def test_get_records(self):
        fields = ["grade", "book", "year", "category", "type", "subject", "author"]
        response = client.post("/datasets/scl", json={"limit": 2, "with_header": True})
        assert response.status_code == 200
        for record in response.json():
            assert isinstance(record, dict)
            assert all(field in record.keys() for field in fields)

    @pytest.mark.parametrize("grade, expected", [(1, 179)])
    def test_get_records_grade(self, grade, expected):
        response = client.post("/datasets/scl", json={"grade": grade})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "book, expected", [("Родная речь. Книга для чтения в I классе начальной школы", 179)]
    )
    def test_get_records_book(self, book, expected):
        response = client.post("/datasets/scl", json={"book": book})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("year, expected", [(1963, 179)])
    def test_get_records_year(self, year, expected):
        response = client.post("/datasets/scl", json={"year": year})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("category, expected", [("Лето", 13), ("Весна", 53), ("Зима", 21)])
    def test_get_records_category(self, category, expected):
        response = client.post("/datasets/scl", json={"category": category})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "text_type, expected", [("Рассказ", 109), ("Басня", 4), ("Стихотворение", 37)]
    )
    def test_get_records_text_type(self, text_type, expected):
        response = client.post("/datasets/scl", json={"text_type": text_type})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("subject, expected", [("Лиса", 6), ("Погляди", 3), ("Ленин", 6)])
    def test_get_records_subject(self, subject, expected):
        response = client.post("/datasets/scl", json={"subject": subject})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "author, expected", [("Скребицкий", 10), ("Михалков", 4), ("Чуковский", 1)]
    )
    def test_get_records_author(self, author, expected):
        response = client.post("/datasets/scl", json={"author": author})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "bad_filter",
        [
            {"grade": 99},
            {"text_type": "Сталин"},
            {"min_len": -1},
            {"max_len": -1},
            {"min_len": 10, "max_len": 5},
        ],
    )
    def test_bad_filters(self, bad_filter):
        with pytest.raises(ValueError):
            response = client.post("/datasets/scl", json={**bad_filter})
            assert response.status_code == 404


class TestStalinWorks:
    def test_get_texts(self):
        response = client.post("/datasets/sw", json={"limit": 2})
        assert response.status_code == 200
        for text in response.json():
            assert isinstance(text, str)

    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_get_texts_limit(self, limit):
        response = client.post("/datasets/sw", json={"limit": limit})
        assert response.status_code == 200
        assert sum(1 for _ in response.json()) == limit

    @pytest.mark.parametrize("min_len", [100, 200, 1000])
    def test_get_texts_min_len(self, min_len):
        response = client.post("/datasets/sw", json={"limit": 5, "min_len": min_len})
        assert response.status_code == 200
        assert all(len(text) >= min_len for text in response.json())

    @pytest.mark.parametrize("max_len", [250, 500, 1000])
    def test_get_texts_max_len(self, max_len):
        response = client.post("/datasets/sw", json={"limit": 5, "max_len": max_len})
        assert response.status_code == 200
        assert all(len(text) < max_len for text in response.json())

    def test_get_records(self):
        fields = ["volume", "year", "type", "is_translation", "source", "subject", "topic"]
        response = client.post("/datasets/sw", json={"limit": 2, "with_header": True})
        assert response.status_code == 200
        for record in response.json():
            assert isinstance(record, dict)
            assert all(field in record.keys() for field in fields)

    @pytest.mark.parametrize("volume, expected", [(1, 62), (5, 63), (10, 38)])
    def test_get_records_volume(self, volume, expected):
        response = client.post("/datasets/sw", json={"volume": volume})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("year, expected", [(1917, 124), (1937, 14), (1945, 22)])
    def test_get_records_year(self, year, expected):
        response = client.post("/datasets/sw", json={"year": year})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "text_type, expected", [("Доклад", 367), ("Письмо", 101), ("Телеграмма", 20)]
    )
    def test_get_records_text_type(self, text_type, expected):
        response = client.post("/datasets/sw", json={"text_type": text_type})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("is_translation, expected", [(True, 63), (False, 1180)])
    def test_get_records_is_translation(self, is_translation, expected):
        response = client.post("/datasets/sw", json={"is_translation": is_translation})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "source, expected", [("Правда", 692), ("Большевик", 49), ("Коммунист", 42)]
    )
    def test_get_records_source(self, source, expected):
        response = client.post("/datasets/sw", json={"source": source})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "subject, expected", [("Съезд", 161), ("Интервью", 3), ("Приветствие", 20)]
    )
    def test_get_records_subject(self, subject, expected):
        response = client.post("/datasets/sw", json={"subject": subject})
        assert len(response.json()) == expected

    @pytest.mark.parametrize("topic, expected", [("I", 330), ("2", 38), ("Доклад", 18)])
    def test_get_records_topic(self, topic, expected):
        response = client.post("/datasets/sw", json={"topic": topic})
        assert len(response.json()) == expected

    @pytest.mark.parametrize(
        "bad_filter",
        [
            {"volume": 99},
            {"text_type": "Фильм"},
            {"min_len": -1},
            {"max_len": -1},
            {"min_len": 10, "max_len": 5},
        ],
    )
    def test_bad_filters(self, bad_filter):
        with pytest.raises(ValueError):
            response = client.post("/datasets/sw", json={**bad_filter})
            assert response.status_code == 404
