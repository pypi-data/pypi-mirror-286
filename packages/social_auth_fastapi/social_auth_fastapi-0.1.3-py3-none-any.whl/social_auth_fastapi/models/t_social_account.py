#!/usr/bin/env python3

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .helper import generate_uuid
from ..models.base import Base, id_key


class SocialAccount(Base):
    """User table"""

    __tablename__ = 't_social_accounts'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=generate_uuid, unique=True)
    login_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment='Username')
    password: Mapped[str] = mapped_column(String(255), comment='Password')
    provider: Mapped[str] = mapped_column(String(255), comment='Provider')
    user_id: Mapped[str] = mapped_column(String(255), nullable=True)
