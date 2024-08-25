from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session

from app.utils.enum import Language

from app.infrastructures.database import get_db

from app.schemas.response.company import (
    CompanyAutoCompleteOutSchema,
    CompanySearchNameOutSchema,
    CompanySearchTagOutSchema,
)
from app.schemas.request.company import NewCompanyInSchema, NewCompanyTagNameInSchema

from app.services.company import CompanyService


router = APIRouter(prefix="")

_company_service = CompanyService()


@router.get("/search")
def autocomplete_company(
    query: str = "",
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
) -> list[CompanyAutoCompleteOutSchema]:
    return _company_service.autocomplete_company_by_word(
        db=db,
        word=query,
        lang=lang,
    )


@router.get("/companies/{company_name}")
async def search_company(
    company_name: str = "",
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
) -> CompanySearchNameOutSchema:
    return _company_service.search_company_by_name(
        db=db,
        name=company_name,
        lang=lang,
    )


@router.post("/companies")
async def add_company(
    new_company: NewCompanyInSchema,
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
):
    return _company_service.add_new_company(db=db, company=new_company, lang=lang)


@router.get("/tags")
async def search_tag_company(
    query: str = "",
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
) -> list[CompanySearchTagOutSchema]:
    return _company_service.search_company_by_tag(
        db=db,
        tag=query,
        lang=lang,
    )


@router.put("/companies/{company_name}/tags")
async def add_company_new_tag(
    tags: list[NewCompanyTagNameInSchema],
    company_name: str = "",
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
):
    return _company_service.add_company_new_tag(
        db=db,
        tags=tags,
        name=company_name,
        lang=lang,
    )


@router.delete("/companies/{company_name}/tags/{tag_name}")
async def delete_company_tag(
    company_name: str = "",
    tag_name: str = "",
    lang: str = Header(default=Language.ko.value, alias="x-wanted-language"),
    db: Session = Depends(get_db),
):
    return _company_service.delete_company_tag(
        db=db,
        name=company_name,
        tag=tag_name,
        lang=lang,
    )
