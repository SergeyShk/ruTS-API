from typing import Any

from fastapi import APIRouter
from ruts import SentsExtractor, WordsExtractor

router = APIRouter(
    prefix="/extract",
    tags=["extract"],
    responses={404: {"description": "Not found"}},
)


@router.get("/sents", summary="Извлечение предложений из текста")
async def extract_sents(text: str) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого извлекаются предложения
    """
    se = SentsExtractor()
    return se.extract(text)


@router.get("/words", summary="Извлечение слов из текста")
async def extract_words(text: str) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого извлекаются слова
    """
    we = WordsExtractor()
    return we.extract(text)
