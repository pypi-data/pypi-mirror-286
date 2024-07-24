#!/usr/bin/env python3
from pydantic import BaseModel


class LoginParam(BaseModel):
    username: str
    password: str
