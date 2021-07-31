from typing import Any

from fastapi import APIRouter, HTTPException
from ruts import DiversityStats
from ruts.constants import DIVERSITY_STATS_DESC

router = APIRouter(
    prefix="/ds",
    tags=["ds"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Получение вычисленных метрик")
async def get_stats(text: str) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    """
    ds = DiversityStats(text)
    return ds.get_stats()


@router.get("/{stat}", summary="Получение определенной метрики")
async def get_stat(text: str, stat: str) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются метрики
    - **stat**: наименование метрики, одно из:
        - **ttr**: Type-Token Ratio (TTR)
        - **rttr**: Root Type-Token Ratio (RTTR)
        - **cttr**: Corrected Type-Token Ratio (CTTR)
        - **httr**: Herdan Type-Token Ratio (HTTR)
        - **sttr**: Summer Type-Token Ratio (STTR)
        - **mttr**: Mass Type-Token Ratio (MTTR)
        - **dttr**: Dugast Type-Token Ratio (DTTR)
        - **mattr**: Moving Average Type-Token Ratio (MATTR)
        - **msttr**: Mean Segmental Type-Token Ratio (MSTTR)
        - **mtld**: Measure of Textual Lexical Diversity (MTLD)
        - **mamtld**: Moving Average Measure of Textual Lexical Diversity (MTLD)
        - **hdd**: Hypergeometric Distribution D (HD-D)
        - **simpson_index**: Индекс Симпсона
        - **hapax_index**: Гапакс-индекс
    """
    ds = DiversityStats(text)
    if stat not in DIVERSITY_STATS_DESC:
        raise HTTPException(status_code=404, detail="Некорректно указана метрика")
    return getattr(ds, stat)
