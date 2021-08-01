from fastapi import FastAPI

from .routers import basic_stats, diversity_stats, extractors, morph_stats, readability_stats

tags_metadata = [
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
        "name": "extract",
        "description": "Извлечение предложений и слов из текста.",
    },
]

api = FastAPI(
    title="ruTS-API",
    description="API для библиотеки ruTS",
    version="0.5.0",
    openapi_tags=tags_metadata,
)


api.include_router(basic_stats.router)
api.include_router(morph_stats.router)
api.include_router(readability_stats.router)
api.include_router(diversity_stats.router)
api.include_router(extractors.router)


@api.get("/")
async def root():
    return {"message": "API для библиотеки ruTS"}
