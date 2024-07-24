#!/usr/bin/env python3
from datetime import UTC, datetime
from datetime import timezone as tzz
from typing import Annotated, Any

from dateutil.parser import parse
from pydantic import AfterValidator, AwareDatetime, BeforeValidator, PlainSerializer, WithJsonSchema

from conf import settings


class TimeZone:
    def __init__(self, tz: str = None):
        self.tz_info = UTC

    def now(self) -> datetime:
        """
        Get time zone time

        :return:
        """
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        datetime Time to time zone time

        :param dt:
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        Convert time string to time zone

        :param date_str:
        :param format_str:
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    def f_timestamp(self, timestamp: int) -> datetime:
        """
        Convert timestamp to time zone

        :param timestamp:
        :return:
        """
        timestamp = int(timestamp) / 1000 if len(str(timestamp)) == 13 else int(timestamp)
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def f_datetime_t_timestamp(dt: datetime) -> int:
        """
        Convert datetime to timestamp

        :param dt:
        :return:
        """
        return int(dt.timestamp() * 1000)

    @staticmethod
    def fix_postgres_datetime(v: str) -> str:
        if isinstance(v, str):
            if '+' in v:
                dt, tz = v.split('+')
                if len(tz) == 2:
                    return f'{dt}+{tz}:00'
        return v

    def validate_timestamp(self, v: Any) -> int:
        """Make from naive datetime a timezone aware (with UTC timezone)."""
        if isinstance(v, (float, int)) or (isinstance(v, str) and v.isnumeric()):
            # parse value to datetime
            v = self.f_timestamp(int(v))
        if isinstance(v, str):
            try:
                v = self.f_str(self.fix_postgres_datetime(v), '%Y-%m-%d %H:%M:%S.%f%z')
            except ValueError:
                v = self.f_str(self.fix_postgres_datetime(v), '%Y-%m-%d %H:%M:%S%z')
        # if datetime is naive, just replace it to UTC
        if v.tzinfo is None:
            result = v.replace(tzinfo=UTC)
        # else convert to utc
        else:
            result = v.astimezone(UTC)

        return int(result.timestamp() * 1000)

    @staticmethod
    def validate_utc(dt: AwareDatetime) -> AwareDatetime:
        """Validate that the pydantic.AwareDatetime is in UTC."""
        if dt.tzinfo.utcoffset(dt) != tzz.utc.utcoffset(dt):
            raise ValueError('Timezone must be UTC')
        return dt

    def convert_datetime_string_to_timezone(self, datetime_str: str) -> datetime:
        return parse(datetime_str).astimezone(tz=self.tz_info)


timezone: TimeZone = TimeZone()

DatetimeUTC = Annotated[
    AwareDatetime, AfterValidator(timezone.validate_utc), BeforeValidator(timezone.fix_postgres_datetime)
]

Timestamp = Annotated[
    int,
    PlainSerializer(func=lambda val: val, return_type=int),
    BeforeValidator(func=lambda val: timezone.validate_timestamp(v=val)),
    WithJsonSchema(
        json_schema={'type': 'number', 'examples': [1704067200000.345, 1704067200000], 'example': 1704067200000.785},
        mode='serialization',
    ),
]
