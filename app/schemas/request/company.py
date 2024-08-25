from pydantic import BaseModel


class NewCompanyTagNameInSchema(BaseModel):
    tag_name: dict[str, str]


class NewCompanyInSchema(BaseModel):
    company_name: dict[str, str]
    tags: list[NewCompanyTagNameInSchema]
