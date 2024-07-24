#!/usr/bin/env python3
from enum import Enum
from enum import IntEnum as SourceIntEnum


class _EnumBase:
    @classmethod
    def get_member_keys(cls: type[Enum]) -> list[str]:
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: type[Enum]) -> list:
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    """Integer enum"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """String enum"""

    pass


class BuildTreeType(StrEnum):
    """Build tree structure type"""

    traversal = 'traversal'
    recursive = 'recursive'
