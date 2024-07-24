#!/usr/bin/env python3
from typing import Annotated

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from core.utils.timezone import DatetimeUTC, timezone

# Universal Mapped type primary key, needs to be added manually, refer to the following usage methods
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='Primary key id')
]


# Mixin: An object-oriented programming concept that makes structures clearer,
# `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """User Mixin data class"""

    create_user: Mapped[int] = mapped_column(sort_order=998, comment='Creator')
    update_user: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Editor')


class DateTimeMixin(MappedAsDataclass):
    """Date and time Mixin data class"""

    created_time: Mapped[DatetimeUTC] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment='Creation time',
    )
    updated_time: Mapped[DatetimeUTC | None] = mapped_column(
        type_=TIMESTAMP(timezone=True), init=False, onupdate=timezone.now, sort_order=999, comment='Update time'
    )


class MappedBase(DeclarativeBase):
    """
    Declarative base class, the original DeclarativeBase class,
    exists as the parent class of all base or data model classes

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declarative data class base class, which will come with data class integration,
    allowing more advanced configuration, but you must pay attention to some of its characteristics,
    especially when used with DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Declarative Mixin data class base class, with data class integration, and contains
    MiXin data class basic table structure, you can simply understand it as a data class base class
    containing basic table structure
    """

    __abstract__ = True
