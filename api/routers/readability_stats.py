from fastapi import APIRouter, HTTPException
from ruts import ReadabilityStats
from ruts.constants import READABILITY_STATS_DESC

router = APIRouter(
    prefix="/rs",
    tags=["rs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Получение вычисленных метрик")
async def get_stats(text: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    """
    rs = ReadabilityStats(text)
    return rs.get_stats()


@router.get("/{stat}", summary="Получение определенной метрики")
async def get_stat(text: str, stat: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются метрики
    - **stat**: наименование метрики, одно из:
        - **calc_flesch_kincaid_grade**: Тест Флеша-Кинкайда
        - **flesch_reading_easy**: Индекс удобочитаемости Флеша
        - **coleman_liau_index**: Индекс Колман-Лиау
        - **smog_index**: Индекс SMOG
        - **automated_readability_index**: Автоматический индекс удобочитаемости
        - **lix**: Индекс удобочитаемости LIX
    """
    rs = ReadabilityStats(text)
    if stat not in READABILITY_STATS_DESC:
        raise HTTPException(status_code=404, detail="Некорректно указана метрика")
    return getattr(rs, stat)
