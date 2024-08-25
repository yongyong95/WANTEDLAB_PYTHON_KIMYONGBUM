from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructures.database import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(50), nullable=True)

    tags = relationship("CompanyTag", back_populates="company")


class CompanyName(Base):
    __tablename__ = "company_name"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    c_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))
    lang: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    c_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))
    lang: Mapped[str] = mapped_column(String(20), nullable=False)
    tag: Mapped[str] = mapped_column(String(100), nullable=False)
    tag_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company_tag_category.id")
    )

    company = relationship("Company", back_populates="tags")
    tag_category = relationship("CompanyTagCategory", back_populates="tags")


class CompanyTagCategory(Base):
    __tablename__ = "company_tag_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

    tags = relationship("CompanyTag", back_populates="tag_category")
