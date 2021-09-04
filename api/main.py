from fastapi import FastAPI
from importlib_metadata import metadata

from .routers import (
    basic_stats,
    datasets,
    diversity_stats,
    extractors,
    morph_stats,
    readability_stats,
)

tags_metadata = [
    {
        "name": "extract",
        "description": "Извлечение предложений и слов из текста.",
    },
    {
        "name": "bs",
        "description": "Вычисление основных статистик текста.",
    },
    {
        "name": "rs",
        "description": "Вычисление метрик удобочитаемости текста.",
    },
    {
        "name": "ms",
        "description": "Вычисление морфологических статистик текста.",
    },
    {
        "name": "ds",
        "description": "Вычисление метрик лексического разнообразия текста.",
    },
    {
        "name": "datasets",
        "description": "Работа с текстовыми наборами данных.",
    },
]

api = FastAPI(
    title="ruTS-API",
    description="API для библиотеки ruTS",
    version="0.8.0",
    openapi_tags=tags_metadata,
)


api.include_router(extractors.router)
api.include_router(basic_stats.router)
api.include_router(morph_stats.router)
api.include_router(readability_stats.router)
api.include_router(diversity_stats.router)
api.include_router(datasets.router)


@api.get("/")
async def root():
    return {"message": "API для библиотеки ruTS"}


@api.get("/version", summary="Версия библиотеки")
async def version():
    return {"ruts": metadata("ruts").json["version"]}


@api.get("/about", summary="Описание проекта")
async def about():
    return {
        k: v
        for k, v in metadata("ruts").json.items()
        if k
        in (
            "name",
            "version",
            "summary",
            "home_page",
            "author",
            "author_email",
            "license",
            "keywords",
        )
    }
