from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import company

tags_metadata = [
    {
        "name": "Company",
        "description": "Company 관련 API 명세",
    },
]


def create_app() -> FastAPI:
    """app 생성"""

    _app = FastAPI(
        openapi_url="/openapi.json",
        openapi_tags=tags_metadata,
        docs_url="/docs",
        redoc_url=None,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(company.router)
    return _app


app = create_app()
