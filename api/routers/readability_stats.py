from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ruts import ReadabilityStats
from ruts.constants import READABILITY_STATS_DESC

router = APIRouter(
    prefix="/rs",
    tags=["rs"],
    responses={404: {"description": "Not found"}},
)


class ItemReadability(BaseModel):
    text: str
    stat: Optional[str] = ""

    class Config:
        schema_extra = {
            "example": {
                "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
                "stat": "",
            }
        }


@router.post("/", summary="Получение вычисленных статистик")
async def get_stats(item: ItemReadability) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **stat**: наименование метрики, одно из:
        - **calc_flesch_kincaid_grade**: Тест Флеша-Кинкайда
        - **flesch_reading_easy**: Индекс удобочитаемости Флеша
        - **coleman_liau_index**: Индекс Колман-Лиау
        - **smog_index**: Индекс SMOG
        - **automated_readability_index**: Автоматический индекс удобочитаемости
        - **lix**: Индекс удобочитаемости LIX
    """
    rs = ReadabilityStats(item.text)
    if not item.stat:
        return rs.get_stats()
    elif item.stat in READABILITY_STATS_DESC:
        return getattr(rs, item.stat)
    else:
        raise HTTPException(status_code=404, detail="Некорректно указана метрика")
