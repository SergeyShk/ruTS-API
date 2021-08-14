from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ruts import DiversityStats
from ruts.constants import DIVERSITY_STATS_DESC

router = APIRouter(
    prefix="/ds",
    tags=["ds"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
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
async def get_stats(item: Item) -> Any:
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
    ds = DiversityStats(item.text)
    if not item.stat:
        return ds.get_stats()
    elif item.stat in DIVERSITY_STATS_DESC:
        return getattr(ds, item.stat)
    else:
        raise HTTPException(status_code=404, detail="Некорректно указана метрика")
