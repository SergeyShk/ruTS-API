from typing import Any, List, Optional, Tuple

from fastapi import APIRouter
from pydantic import BaseModel
from ruts import SentsExtractor, WordsExtractor

router = APIRouter(
    prefix="/extract",
    tags=["extract"],
    responses={404: {"description": "Not found"}},
)


class ItemSents(BaseModel):
    text: str
    min_len: Optional[int] = 0
    max_len: Optional[int] = 0

    class Config:
        schema_extra = {
            "example": {
                "text": "Да. Времена изменились. Дети больше не слушаются своих родителей, и каждый пишет книги.",
                "min_len": 5,
                "max_len": 0,
            }
        }


class ItemWords(BaseModel):
    text: str
    filter_punct: Optional[int] = True
    filter_nums: Optional[int] = False
    use_lexemes: Optional[int] = False
    stopwords: Optional[List[str]] = None
    lowercase: Optional[int] = False
    ngram_range: Optional[Tuple[int, int]] = (1, 1)
    min_len: Optional[int] = 0
    max_len: Optional[int] = 0
    most_common: Optional[int] = 0

    class Config:
        schema_extra = {
            "example": {
                "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
                "filter_punct": True,
                "filter_nums": False,
                "use_lexemes": True,
                "stopwords": ["кто", "в", "тот"],
                "lowercase": True,
                "ngram_range": (2, 2),
                "min_len": 0,
                "max_len": 0,
                "most_common": 0,
            }
        }


@router.post("/sents", summary="Извлечение предложений из текста")
async def extract_sents(item: ItemSents) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого извлекаются предложения
    - **min_len**: минимальная длина извлекаемого предложения
    - **max_len**: максимальная длина извлекаемого предложения
    """
    se = SentsExtractor(min_len=item.min_len, max_len=item.max_len)
    return se.extract(item.text)


@router.post("/words", summary="Извлечение слов из текста")
async def extract_words(item: ItemWords) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого извлекаются слова
    - **filter_punct**: фильтровать знаки препинания
    - **filter_nums**: фильтровать числа
    - **use_lexemes**: использовать леммы слов
    - **stopwords**: список стоп-слов
    - **lowercase**: конвертировать слова в нижний регистр
    - **ngram_range**: нижняя и верхняя граница размера N-грамм
    - **min_len**: минимальная длина извлекаемого слова
    - **max_len**: максимальная длина извлекаемого слова
    - **most_common**: количество топ-слов
    """
    we = WordsExtractor(
        filter_punct=item.filter_punct,
        filter_nums=item.filter_nums,
        use_lexemes=item.use_lexemes,
        stopwords=item.stopwords,
        lowercase=item.lowercase,
        ngram_range=item.ngram_range,
        min_len=item.min_len,
        max_len=item.max_len,
    )
    words = we.extract(item.text)
    if not item.most_common:
        return words
    else:
        return we.get_most_common(item.most_common)
