from fastapi import FastAPI

from .routers import basic_stats, morph_stats, readability_stats

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
]

api = FastAPI(
    title="ruTS-API",
    description="API для библиотеки ruTS",
    version="0.2.0",
    openapi_tags=tags_metadata,
)


api.include_router(basic_stats.router)
api.include_router(morph_stats.router)
api.include_router(readability_stats.router)


@api.get("/")
async def root():
    return {"message": "API для библиотеки ruTS"}
