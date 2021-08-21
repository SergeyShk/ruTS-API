from typing import Any, Optional, Tuple

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from ruts import MorphStats
from ruts.constants import MORPHOLOGY_STATS_DESC

router = APIRouter(
    prefix="/ms",
    tags=["ms"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    text: str
    filter_none: Optional[bool] = False
    stats: Tuple[str, ...] = Query(None, description="Кортеж выбранных статистик")

    class Config:
        schema_extra = {
            "example": {
                "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
                "filter_none": True,
                "stats": ("pos", "case"),
            }
        }


@router.post("/", summary="Получение вычисленных статистик")
async def get_stats(item: Item) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **filter_none**: фильтровать пустые значения
    - **stats**: кортеж выбранных статистик:
        - **tags**: тэг OpenCorpora
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
    ms = MorphStats(item.text)
    if not item.stats:
        return ms.get_stats(filter_none=item.filter_none)
    elif all(stat in MORPHOLOGY_STATS_DESC for stat in item.stats):
        stats = ms.get_stats(*item.stats, filter_none=item.filter_none)
        if len(item.stats) == 1:
            return stats[item.stats[0]]
        else:
            return stats
    else:
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")


@router.post("/explain", summary="Разбор текста по морфологическим статистикам")
async def explain_text(item: Item) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **filter_none**: фильтровать пустые значения
    - **stats**: кортеж выбранных статистик:
        - **tags**: тэг OpenCorpora
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
    ms = MorphStats(item.text)
    if not item.stats:
        return ms.explain_text(filter_none=item.filter_none)
    elif all(stat in MORPHOLOGY_STATS_DESC for stat in item.stats):
        return ms.explain_text(*item.stats, filter_none=item.filter_none)
    else:
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")
