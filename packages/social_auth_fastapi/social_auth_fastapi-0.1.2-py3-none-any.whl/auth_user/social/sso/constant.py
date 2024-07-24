from enum import Enum


class ProviderEnum(str, Enum):
    FACEBOOK: str = 'facebook'
    GITHUB: str = 'github'
    GOOGLE: str = 'google'
    FITBIT: str = 'fitbit'
    GENERIC: str = 'generic'
    GITLAB: str = 'gitlab'
    KAKAO: str = 'kakao'
    LINE: str = 'line'
    LINKEDIN: str = 'linkedin'
    MICROSOFT: str = 'microsoft'
    NAVER: str = 'naver'
    NOTION: str = 'notion'
    SPOTIFY: str = 'spotify'
    TWITTER: str = 'twitter'
    YANDEX: str = 'yandex'
