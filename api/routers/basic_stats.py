from fastapi import APIRouter, HTTPException
from ruts import BasicStats
from ruts.constants import BASIC_STATS_DESC

router = APIRouter(
    prefix="/bs",
    tags=["bs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Получение вычисленных статистик")
async def get_stats(text: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    """
    bs = BasicStats(text)
    return bs.get_stats()


@router.get("/{stat}", summary="Получение определенной статистики")
async def get_stat(text: str, stat: str):
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **stat**: наименование статистики, одно из:
        - **n_sents**: предложения
        - **n_words**: слова
        - **n_unique_words**: уникальные слова
        - **n_long_words**: длинные слова
        - **n_complex_words**: сложные слова
        - **n_simple_words**: простые слова
        - **n_monosyllable_words**: односложные слова
        - **n_polysyllable_words**: многосложные слова
        - **n_chars**: символы
        - **n_letters**: буквы
        - **n_spaces**: пробелы
        - **n_syllables**: слоги
        - **n_punctuations**: знаки препинания
    """
    if stat not in BASIC_STATS_DESC:
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")
    bs = BasicStats(text)
    return bs.get_stats()[stat]
