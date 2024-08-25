import operator
from itertools import groupby

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.enum import Language

from app.repositories.company import CompanyRepository


class CompanyService:
    _company_repo = CompanyRepository()

    def autocomplete_company_by_word(self, db: Session, word: str, lang: Language):
        company_ids = [
            id_tuple[0]
            for id_tuple in self._company_repo.get_company_ids_by_word(
                db=db,
                search=word,
            )
        ]
        company_names = self._company_repo.get_company_names_by_ids_with_lang(
            db=db, c_ids=company_ids, lang=lang
        )
        return [{"company_name": c.name} for c in company_names]

    def search_company_by_name(self, db: Session, name: str, lang: Language):
        company_id = self._company_repo.get_company_id_by_name(
            db=db,
            name=name,
        )
        if not company_id:
            raise HTTPException(status_code=404, detail="Company not found")

        company_name = self._company_repo.get_company_name_by_id_with_lang(
            db=db, c_id=company_id[0], lang=lang
        )[0]
        company_tags = self._company_repo.get_company_tags_by_id_with_lang(
            db=db, c_id=company_id[0], lang=lang
        )
        return {
            "company_name": company_name,
            "tags": [tag_tuple[0] for tag_tuple in company_tags],
        }

    def search_company_by_tag(self, db: Session, tag: str, lang: Language):
        results = []

        company_ids = [
            id_tuple[0]
            for id_tuple in self._company_repo.get_company_ids_by_tag(
                db=db,
                tag=tag,
            )
        ]
        company_names = self._company_repo.get_company_names_by_ids(
            db=db, c_ids=company_ids
        )

        company_names_list = [
            {"id": c.c_id, "lang": c.lang, "name": c.name} for c in company_names
        ]
        company_names_sorted = sorted(company_names_list, key=lambda x: x["id"])
        company_names_dict = {
            key: list(value)
            for key, value in groupby(company_names_sorted, operator.itemgetter("id"))
        }

        for _, items in company_names_dict.items():
            ko_name = list(set(item["name"] for item in items if item["lang"] == "ko"))
            etc_name = list(set(item["name"] for item in items if item["lang"] != "ko"))

            if ko_name:
                results.append({"company_name": ko_name[0]})
            elif etc_name:
                results.append({"company_name": etc_name[0]})

        print(results)
        return results

    def add_new_company(
        self,
        db: Session,
        company: dict[dict[str, str], list[dict[str, str]]],
        lang: str,
    ):
        company_id = self._company_repo.insert_new_company(
            db=db, company_name=company.company_name
        )
        if not company_id:
            raise HTTPException(status_code=500, detail="Error adding new company")

        new_company_name_add_ok = self._company_repo.insert_new_company_name(
            db=db, c_id=company_id, company_name=company.company_name
        )
        if not new_company_name_add_ok:
            raise HTTPException(
                status_code=500, detail="Error adding new company names"
            )

        new_tag_category_add_ok = self._company_repo.insert_new_tag_category(
            db=db, tags=company.tags
        )
        if not new_tag_category_add_ok:
            raise HTTPException(
                status_code=400, detail="Error adding new tag categories"
            )

        new_tag_add_ok = self._company_repo.upsert_company_new_tags_by_id(
            db=db, c_id=company_id, tags=company.tags
        )
        if not new_tag_add_ok:
            raise HTTPException(status_code=400, detail="Error adding new tags")

        company_name = self._company_repo.get_company_name_by_id_with_lang(
            db=db, c_id=company_id, lang=lang
        )[0]
        company_tags = self._company_repo.get_company_tags_by_id_with_lang(
            db=db, c_id=company_id, lang=lang
        )
        return {
            "company_name": company_name,
            "tags": [tag_tuple[0] for tag_tuple in company_tags],
        }

    def add_company_new_tag(
        self, db: Session, tags: list[dict[str, str]], name: str, lang: Language
    ):
        company_id = self._company_repo.get_company_id_by_name(db=db, name=name)
        if not company_id:
            raise HTTPException(status_code=404, detail="Company not found")

        new_tag_category_add_ok = self._company_repo.insert_new_tag_category(
            db=db, tags=tags
        )
        if not new_tag_category_add_ok:
            raise HTTPException(
                status_code=400, detail="Error adding new tag categories"
            )

        new_tag_add_ok = self._company_repo.upsert_company_new_tags_by_id(
            db=db, c_id=company_id[0], tags=tags
        )
        if not new_tag_add_ok:
            raise HTTPException(status_code=400, detail="Error adding new tags")

        company_name = self._company_repo.get_company_name_by_id_with_lang(
            db=db, c_id=company_id[0], lang=lang
        )[0]
        company_tags = self._company_repo.get_company_tags_by_id_with_lang(
            db=db, c_id=company_id[0], lang=lang
        )
        return {
            "company_name": company_name,
            "tags": [tag_tuple[0] for tag_tuple in company_tags],
        }

    def delete_company_tag(self, db: Session, tag: str, name: str, lang: Language):
        company_id = self._company_repo.get_company_id_by_name(
            db=db,
            name=name,
        )
        if not company_id:
            raise HTTPException(status_code=404, detail="Company not found")
        company_id = company_id[0]

        tag_category_id = self._company_repo.get_tag_category_id_by_tag(
            db=db, c_id=company_id, tag=tag
        )
        if not tag_category_id:
            raise HTTPException(status_code=400, detail="Tag category not found")
        tag_category_id = tag_category_id[0]

        delete_tag_ok = self._company_repo.delete_company_tag_by_tag_category_id(
            db=db,
            c_id=company_id,
            tag_category_id=tag_category_id,
        )
        company_name = self._company_repo.get_company_name_by_id_with_lang(
            db=db, c_id=company_id, lang=lang
        )[0]
        company_tags = self._company_repo.get_company_tags_by_id_with_lang(
            db=db, c_id=company_id, lang=lang
        )
        return {
            "company_name": company_name,
            "tags": [tag_tuple[0] for tag_tuple in company_tags],
        }
