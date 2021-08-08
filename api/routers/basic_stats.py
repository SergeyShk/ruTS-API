from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ruts import BasicStats

router = APIRouter(
    prefix="/bs",
    tags=["bs"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    text: str
    normalize: Optional[bool] = False
    stat: Optional[str] = ""


@router.post("/", summary="Получение вычисленных статистик")
async def get_stats(item: Item) -> Any:
    """
    Аргументы:

    - **text**: текст, для которого вычисляются статистики
    - **normalize**: вычислять нормализованные статистики
    - **stat**: наименование конкретной статистики, одно из:
        - **c_letters**: распределение слов по количеству букв
        - **c_syllables**: распределение слов по количеству слогов
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
        - **p_unique_words**: нормализованное количество уникальных слов
        - **p_long_words**: нормализованное количество длинных слов
        - **p_complex_words**: нормализованное количество сложных слов
        - **p_simple_words**: нормализованное количество простых слов
        - **p_monosyllable_words**: нормализованное количество односложных слов
        - **p_polysyllable_words**: нормализованное количество многосложных слов
        - **p_letters**: нормализованное количество букв
        - **p_spaces**: нормализованное количество пробелов
        - **p_punctuations**: нормализованное количество знаков препинания
    """
    bs = BasicStats(item.text, normalize=item.normalize)
    stats = bs.get_stats()
    if not item.stat:
        return stats
    elif item.stat in bs.__dict__:
        return stats[item.stat]
    else:
        raise HTTPException(status_code=404, detail="Некорректно указана статистика")
