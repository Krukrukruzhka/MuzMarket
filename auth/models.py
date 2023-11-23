from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, metadata
from src.models import role, region


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    firstname: str = Column("firstname", String, nullable=False)
    region_id: int = Column("region_id", Integer, ForeignKey(region.c.id))
    role_id: int = Column("role_id", Integer, ForeignKey(role.c.id), default=1)

