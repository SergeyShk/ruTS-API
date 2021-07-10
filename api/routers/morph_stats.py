from typing import Tuple

from fastapi import APIRouter, HTTPException, Query
from ruts import MorphStats
from ruts.constants import MORPHOLOGY_STATS_DESC

router = APIRouter(
    prefix="/ms",
    tags=["ms"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Получение вычисленных статистик")
async def get_stats(text: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    """
    ms = MorphStats(text)
    return ms.get_stats()


@router.get("/explain", summary="Разбор текста по морфологическим статистикам")
async def explain_text(
    text: str,
    stats: Tuple[str, ...] = Query(None, description="Кортеж выбранных статистик"),
    filter_none: bool = False,
):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **stats**: кортеж выбранных статистик из следующих:
        - **pos**: часть речи
        - **animacy**: одушевленность
        - **aspect**: вид
        - **case**: падеж
        - **gender**: пол
        - **involvement**: совместность
        - **mood**: наклонение
        - **number**: число
        - **person**: лицо
        - **tense**: время
        - **transitivity**: переходность
        - **voice**: залог
    - **filter_none**: фильтровать пустые значения
    """
    if not all(stat in MORPHOLOGY_STATS_DESC for stat in stats):
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")
    ms = MorphStats(text)
    return ms.explain_text(*stats, filter_none=filter_none)


@router.get("/{stat}", summary="Получение определенной статистики")
async def get_stat(text: str, stat: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **stat**: наименование статистики, одно из:
        - **pos**: часть речи
        - **animacy**: одушевленность
        - **aspect**: вид
        - **case**: падеж
        - **gender**: пол
        - **involvement**: совместность
        - **mood**: наклонение
        - **number**: число
        - **person**: лицо
        - **tense**: время
        - **transitivity**: переходность
        - **voice**: залог
    """
    if stat not in MORPHOLOGY_STATS_DESC:
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")
    ms = MorphStats(text)
    return ms.get_stats()[stat]
