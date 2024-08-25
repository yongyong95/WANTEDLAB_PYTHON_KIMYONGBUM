from pydantic import BaseModel, ConfigDict


class CompanyOutSchema(BaseModel):
    company_name: str = ""

    model_config = ConfigDict(from_attributes=True)


class CompanyAutoCompleteOutSchema(CompanyOutSchema):
    pass


class CompanySearchNameOutSchema(BaseModel):
    company_name: str = ""
    tags: list[str]

    model_config = ConfigDict(from_attributes=True)


class CompanySearchTagOutSchema(CompanyOutSchema):
    pass
