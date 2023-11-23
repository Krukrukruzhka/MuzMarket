from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, REAL, DateTime, ForeignKey, Boolean
from src.database import metadata

region = Table(
    "region",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False, unique=True)
)

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False, unique=True)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstname", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("region_id", Integer, ForeignKey(region.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id), default=1),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

store = Table(
    "store",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("address", String, nullable=False, unique=True),
    Column("phone", String, nullable=False, unique=True),
    Column("region_id", Integer, ForeignKey(region.c.id), nullable=False),
    Column("work_hours", String, nullable=False)
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False, unique=True)
)

subcategory = Table(
    "subcategory",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("category_id", Integer, ForeignKey(category.c.id), nullable=False),
    Column("endpoint", String, nullable=False, unique=True),
    Column("title", String, nullable=False, unique=True)
)

strainer = Table(
    "strainer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False, unique=True),
)

strainer_subcategory = Table(
    "strainer_subcategory",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("subcategory_id", Integer, ForeignKey(subcategory.c.id), nullable=False),
    Column("strainer_id", Integer, ForeignKey(strainer.c.id), nullable=False)
)


parameter = Table(
    "parameter",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("strainer_id", Integer, ForeignKey(strainer.c.id), nullable=False)
)

item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("subcategory_id", Integer, ForeignKey(subcategory.c.id), nullable=False),
    Column("rate", REAL),
    Column("article", String, nullable=False, unique=True)
)

status = Table(
    "status",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False, unique=True),
)

ordering = Table(
    "ordering",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("store_id", Integer, ForeignKey(store.c.id), nullable=False),
    Column("item_id", Integer, ForeignKey(item.c.id), nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("status_id", Integer, ForeignKey(status.c.id), nullable=False),
    Column("timestamp", DateTime, nullable=False, default=datetime.utcnow()),
    Column("amount", Integer, nullable=False)
)

item_store = Table(
    "item_store",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("store_id", Integer, ForeignKey(store.c.id), nullable=False),
    Column("item_id", Integer, ForeignKey(item.c.id), nullable=False),
    Column("amount", Integer, nullable=False, default=0)
)

item_parameter = Table(
    "item_parameter",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("parameter_id", Integer, ForeignKey(parameter.c.id), nullable=False),
    Column("item_id", Integer, ForeignKey(item.c.id), nullable=False)
)