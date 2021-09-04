from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from ruts.datasets import SovChLit, StalinWorks

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)


class ItemSovChLit(BaseModel):
    grade: Optional[int] = None
    book: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
    text_type: Optional[str] = None
    subject: Optional[str] = None
    author: Optional[str] = None
    min_len: Optional[int] = 0
    max_len: Optional[int] = 0
    limit: Optional[int] = None
    with_header: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "grade": 1,
                "book": "",
                "year": 1963,
                "category": "Зима",
                "text_type": "",
                "subject": "",
                "author": "",
                "min_len": 0,
                "max_len": 300,
                "limit": 5,
                "with_header": False,
            }
        }


class ItemStalinWorks(BaseModel):
    volume: Optional[int] = None
    year: Optional[int] = None
    text_type: Optional[str] = None
    is_translation: Optional[bool] = None
    source: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    min_len: Optional[int] = 0
    max_len: Optional[int] = 0
    limit: Optional[int] = None
    with_header: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "volume": 14,
                "year": 1937,
                "text_type": "Письмо",
                "is_translation": False,
                "source": 'Книга "Иосиф Сталин в объятиях семьи"',
                "subject": "",
                "topic": "",
                "min_len": 0,
                "max_len": 300,
                "limit": 5,
                "with_header": True,
            }
        }


@router.post("/scl", summary="Корпус советских хрестоматий по литературе")
async def get_dataset_scl(item: ItemSovChLit) -> Any:
    """
    Аргументы:
    - **grade**: уровень сложности текстов
    - **book**: наименование книги
    - **year**: год издания книги
    - **category**: категория текстов
    - **text_type**: тип текстов
    - **subject**: наименование текстов
    - **author**: автор текстов
    - **min_len**: минимальная длина текста (в символах)
    - **max_len**: максимальная длина текста (в символах)
    - **limit**: количество текстов
    - **with_header**: выводить заголовок
    """
    dataset = SovChLit()
    params = dict(
        grade=item.grade,
        book=item.book,
        year=item.year,
        category=item.category,
        text_type=item.text_type,
        subject=item.subject,
        author=item.author,
        min_len=item.min_len,
        max_len=item.max_len,
        limit=item.limit,
    )
    if item.with_header:
        return dataset.get_records(**params)
    else:
        return dataset.get_texts(**params)


@router.post("/sw", summary="Полное собрание сочинений И.В. Сталина")
async def get_dataset_sw(item: ItemStalinWorks) -> Any:
    """
    Аргументы:
    - **volume**: номер тома
    - **year**: год издания книги
    - **text_type**: тип текстов
    - **is_translation**: признак перевода
    - **source**: первоначальный источник текстов
    - **subject**: наименование текстов
    - **topic**: наименование подраздела текстов
    - **min_len**: минимальная длина текста (в символах)
    - **max_len**: максимальная длина текста (в символах)
    - **limit**: количество текстов
    - **with_header**: выводить заголовок
    """
    dataset = StalinWorks()
    params = dict(
        volume=item.volume,
        year=item.year,
        text_type=item.text_type,
        is_translation=item.is_translation,
        source=item.source,
        subject=item.subject,
        topic=item.topic,
        min_len=item.min_len,
        max_len=item.max_len,
        limit=item.limit,
    )
    if item.with_header:
        return dataset.get_records(**params)
    else:
        return dataset.get_texts(**params)


@router.get("/", summary="Список наборов данных")
async def version():
    scl = SovChLit()
    sw = StalinWorks()
    return {"svc": scl.info, "sw": sw.info}
