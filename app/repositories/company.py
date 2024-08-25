from sqlite3 import IntegrityError
from fastapi import HTTPException

from sqlalchemy import distinct, exists, or_, select
from sqlalchemy.orm import Session

from app.utils.enum import Language

from app.entities.company import Company, CompanyName, CompanyTag, CompanyTagCategory
from app.infrastructures.database import get_db


class CompanyRepository:

    def get_company_ids_by_word(self, db: Session, search: str):
        """단어 통해 검색된 회사 IDs 리스트 반환"""
        return (
            db.query(CompanyName.c_id)
            .filter(CompanyName.name.like(f"%{search}%"))
            .all()
        )

    def get_company_ids_by_tag(self, db: Session, tag: str):
        """태그 통해 검색된 회사 IDs 리스트 반환"""
        return db.query(distinct(CompanyTag.c_id)).filter(CompanyTag.tag == tag).all()

    def get_company_name_by_id_with_lang(
        self,
        db: Session,
        c_id: int,
        lang: Language,
    ):
        """회사 ID 통해 지원 언어의 회사명 반환"""
        return (
            db.query(CompanyName.name)
            .filter(
                CompanyName.c_id == c_id,
                CompanyName.lang == lang,
            )
            .first()
        )

    def get_company_names_by_ids_with_lang(
        self,
        db: Session,
        c_ids: list[int],
        lang: str,
    ):
        """회사 IDs 통해 검색된 지원 언어 회사명 리스트 반환"""
        return (
            db.query(CompanyName)
            .filter(
                CompanyName.c_id.in_(c_ids),
                CompanyName.lang == lang,
            )
            .all()
        )

    def get_company_names_by_ids(
        self,
        db: Session,
        c_ids: list[int],
    ):
        """회사 IDs 통해 검색된 회사명 리스트 반환"""
        return db.query(CompanyName).filter(CompanyName.c_id.in_(c_ids)).all()

    def get_company_id_by_name(
        self,
        db: Session,
        name: str,
    ):
        """회사명 통해 회사 ID 반환"""
        return (
            db.query(distinct(CompanyName.c_id))
            .filter(CompanyName.name == name)
            .first()
        )

    def get_company_tags_by_id_with_lang(
        self,
        db: Session,
        c_id: int,
        lang: str,
    ):
        """회사 ID 통해 지원 언어의 회사 태그 리스트 반환"""
        return (
            db.query(CompanyTag.tag)
            .filter(
                CompanyTag.c_id == c_id,
                CompanyTag.lang == lang,
            )
            .order_by(CompanyTag.tag_category_id)
            .all()
        )

    def insert_new_company(self, db: Session, company_name: dict[str, str]):
        """입력받은 회사명 통해 새로운 회사 생성"""
        try:
            company = Company()
            for lang, name in company_name.items():
                existed_company = (
                    db.query(Company).filter(Company.company_name == name).first()
                )
                if existed_company:
                    return existed_company.id

                if lang == Language.ko.value:
                    company.company_name = name

            db.add(company)
            db.commit()
            db.refresh(company)
        except Exception as e:
            db.rollback()
            return 0

        return company.id

    def insert_new_company_name(
        self, db: Session, c_id: int, company_name: dict[str, str]
    ):
        """입력받은 회사명 통해 지원 언어별 새로운 회사명 생성"""
        try:
            # 기존 데이터가 남았을 경우, 현재 데이터로 리프레시
            db.query(CompanyName).filter(CompanyName.c_id == c_id).delete(
                synchronize_session="fetch"
            )
            db.commit()

            new_company_names = []
            for lang, name in company_name.items():
                new_company_name = CompanyName(
                    c_id=c_id,
                    lang=lang,
                    name=name,
                )
                new_company_names.append(new_company_name)

            if new_company_names:
                db.bulk_save_objects(new_company_names)
        except Exception as e:
            return False

        return True

    def insert_new_tag_category(self, db: Session, tags: list[dict[str, str]]):
        """입력받은 태그 리스트 통해 새로운 태그 카테고리 생성"""
        try:
            for item in tags:
                for lang, tag_name in item.tag_name.items():
                    if lang == Language.ko.value:
                        tag_category = (
                            db.query(CompanyTagCategory)
                            .filter(CompanyTagCategory.category_name == tag_name)
                            .first()
                        )
                        if not tag_category:
                            new_tag_category = CompanyTagCategory(
                                category_name=tag_name
                            )
                            db.add(new_tag_category)
                            db.commit()
                            db.refresh(new_tag_category)
        except Exception as e:
            return False

        return True

    def upsert_company_new_tags_by_id(
        self, db: Session, c_id: int, tags: list[dict[str, str]]
    ):
        """회사 ID 통해 새로운 회사 태그 리스트 추가"""
        tags_to_update = []
        tags_to_create = []

        for item in tags:
            tags_to_category_update = []
            for lang, tag_name in item.tag_name.items():
                tag_category = (
                    db.query(CompanyTagCategory)
                    .filter(CompanyTagCategory.category_name == tag_name)
                    .first()
                )
                if tag_category:
                    tag_category_id = tag_category.id

                tag = (
                    db.query(CompanyTag)
                    .join(CompanyTag.tag_category)
                    .filter(
                        CompanyTag.c_id == c_id,
                        CompanyTag.lang == lang,
                        CompanyTag.tag == tag_name,
                    )
                    .first()
                )
                # 단순 존재 확인뿐 아니라, 새 태그 이름이 더 최신 데이터일것이라는 전제하에 갱신
                if tag:
                    tag.tag = tag_name
                    tags_to_update.append(tag)
                else:
                    new_tag = CompanyTag(
                        c_id=c_id,
                        lang=lang,
                        tag=tag_name,
                    )
                    tags_to_category_update.append(new_tag)

            # ko 기준으로 생성된 공통 tag_category 를 각 지원언어 같은 category 값으로 넣어줌
            for tag_to_category_update in tags_to_category_update:
                tag_to_category_update.tag_category_id = (
                    tag_category_id if tag_category_id else -1
                )
                tags_to_create.append(tag_to_category_update)

        try:
            if tags_to_update:
                db.bulk_save_objects(tags_to_update)
            if tags_to_create:
                db.bulk_save_objects(tags_to_create)

            db.commit()
        except IntegrityError as e:
            db.rollback()
            return False

        return True

    def get_tag_category_id_by_tag(
        self,
        db: Session,
        c_id: int,
        tag: str,
    ):
        """회사 ID, 회사태그 통해 공통 태그 카테고리 ID 반환"""
        return (
            db.query(CompanyTag.tag_category_id)
            .filter(CompanyTag.c_id == c_id, CompanyTag.tag == tag)
            .first()
        )

    def delete_company_tag_by_tag_category_id(
        self,
        db: Session,
        c_id: int,
        tag_category_id: int,
    ):
        """회사태그 통해 회사에 연결된 일부 태그 삭제"""
        try:
            db.query(CompanyTag).filter(
                CompanyTag.c_id == c_id,
                CompanyTag.tag_category_id == tag_category_id,
            ).delete(synchronize_session="fetch")
            db.commit()
        except Exception as e:
            db.rollback()
            return False

        return True
