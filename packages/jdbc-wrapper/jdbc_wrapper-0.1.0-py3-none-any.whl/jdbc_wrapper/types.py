from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal as _Decimal
from itertools import chain
from typing import TYPE_CHECKING, Any, Generic, cast

import jpype
from jpype import dbapi2 as jpype_dbapi2
from jpype.dbapi2 import JDBCType
from typing_extensions import TypeAlias, TypeVar, override

from jdbc_wrapper.exceptions import Error
from jdbc_wrapper.utils import wrap_errors

try:
    from sqlalchemy import quoted_name
except ImportError:  # pragma: no cover
    quoted_name = str

if TYPE_CHECKING:
    from collections.abc import Mapping

    from _typeshed import Incomplete

    from jdbc_wrapper.abc import TypePipeline

    class ResultSet:
        def __getattr__(self, name: str) -> Any: ...


__all__ = []

_J = TypeVar("_J", bound=JDBCType)
_T = TypeVar("_T")
_DT = TypeVar("_DT", bound="date | time | datetime")
_R = TypeVar("_R", bound=tuple[Any, ...], default=tuple[Any, ...])
_R2 = TypeVar("_R2", bound=tuple[Any, ...])

_registry = {}
_JDBCMeta: TypeAlias = "Incomplete"
_JDBCStmt: TypeAlias = "Incomplete"

Description: TypeAlias = """tuple[
    str, int | str | None, int | None, int | None, int | None, int | None, bool | None
]"""

TypeCodes: Mapping[str, int] = {}


class Query(Generic[_R]):
    __slots__ = ("_statement",)

    def __init__(self, statement: str) -> None:
        self._statement = statement

    @property
    def statement(self) -> str:
        return self._statement

    def as_type(self, dtype: type[_R2]) -> Query[_R2]:
        return self.construct(self._statement, dtype)

    @classmethod
    def construct(cls, statement: str, dtype: type[_R2]) -> Query[_R2]:
        return cls[dtype](statement)  # pyright: ignore[reportReturnType,reportInvalidTypeArguments]


class DateStr(str, Generic[_DT]):
    __slots__ = ("_value", "_dtype", "_date")

    def __init__(self, value: str, dtype: type[_DT]) -> None:
        self._value = value
        self._dtype = dtype
        self._date = dtype.fromisoformat(value)

    @override
    def __new__(cls, value: str, dtype: type[_DT]) -> DateStr[_DT]:
        return super().__new__(cls)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._value, name)

    @override
    def __str__(self) -> str:
        return self._value


class JDBCTypeGetter:
    __slots__ = ("_meta", "_index", "_connection")

    def __init__(
        self,
        meta: _JDBCMeta,
        index: int,
        connection: jpype_dbapi2.Connection | None = None,
    ) -> None:
        self._meta = meta
        self._index = index
        self._connection = connection

    @wrap_errors
    def using_type(self) -> JDBCType:
        return jpype_dbapi2.GETTERS_BY_TYPE(self._connection, self._meta, self._index)

    @wrap_errors
    def using_name(self) -> JDBCType:
        return jpype_dbapi2.GETTERS_BY_NAME(self._connection, self._meta, self._index)


class JDBCTypeSetter:
    __slots__ = ("_meta", "_index", "_python_type", "_connection")

    def __init__(
        self,
        meta: _JDBCMeta | None,
        index: int | None,
        python_type: type[Any] | None,
        connection: jpype_dbapi2.Connection | None = None,
    ) -> None:
        self._meta = meta
        self._index = index
        self._python_type = python_type
        self._connection = connection

    @wrap_errors
    def using_type(self) -> JDBCType | None:
        if self._python_type is None:
            raise AttributeError("Python type not set")
        return jpype_dbapi2.SETTERS_BY_TYPE(
            self._connection, self._meta, self._index, self._python_type
        )

    @wrap_errors
    def using_meta(self) -> JDBCType:
        if self._meta is None or self._index is None:
            raise AttributeError("Meta or index not set")
        return jpype_dbapi2.SETTERS_BY_META(
            self._connection, self._meta, self._index, self._python_type
        )


class WrappedJDBCType(Generic[_J, _T]):
    __slots__ = ("_jdbc_type", "_python_type")

    def __init__(self, jdbc_type: _J, python_type: type[_T] | TypePipeline[_T]) -> None:
        self._jdbc_type = jdbc_type
        self._python_type = python_type

        if self.name and self.type_code:
            type_codes = cast(dict[str, int], TypeCodes)
            type_codes.setdefault(self.name, self.type_code)

        _registry.setdefault(self._jdbc_type, self)

    @property
    def name(self) -> str | None:
        return self._jdbc_type._name  # noqa: SLF001

    @property
    def type_code(self) -> int | None:
        return self._jdbc_type._code  # noqa: SLF001

    @property
    def getter(self) -> str | None:
        return self._jdbc_type._getter  # noqa: SLF001

    @property
    def setter(self) -> str | None:
        return self._jdbc_type._setter  # noqa: SLF001

    @property
    def pipeline(self) -> TypePipeline[_T]:
        from jdbc_wrapper.pipeline import get_type_pipeline

        return get_type_pipeline(self._python_type)

    @wrap_errors
    def get(self, result_set: ResultSet, index: int, is_callable: bool) -> _T:  # noqa: FBT001
        return self._jdbc_type.get(result_set, index, is_callable)

    @wrap_errors
    def set(self, statement: _JDBCStmt, index: int, value: _T) -> Any:
        return self._jdbc_type.set(statement, index, value)

    @override
    def __repr__(self) -> str:
        return repr(self._jdbc_type)

    @override
    def __eq__(self, value: object) -> bool:
        return (
            value == self._jdbc_type
            if isinstance(value, WrappedJDBCType)
            else self._jdbc_type == value
        )

    @override
    def __hash__(self) -> int:
        return hash(self._jdbc_type)


### declare:: start
Array = WrappedJDBCType(jpype_dbapi2.ARRAY, list)
Bigint = WrappedJDBCType(jpype_dbapi2.BIGINT, int)
Bit = WrappedJDBCType(jpype_dbapi2.BIT, bool)
Blob = WrappedJDBCType(jpype_dbapi2.BLOB, bytes)
Boolean = WrappedJDBCType(jpype_dbapi2.BOOLEAN, bool)
Char = WrappedJDBCType(jpype_dbapi2.CHAR, str)
Clob = WrappedJDBCType(jpype_dbapi2.CLOB, str)
Date = WrappedJDBCType(jpype_dbapi2.DATE, date)
Double = WrappedJDBCType(jpype_dbapi2.DOUBLE, float)
Integer = WrappedJDBCType(jpype_dbapi2.INTEGER, int)
Object = WrappedJDBCType(jpype_dbapi2.OBJECT, object)
Longvarchar = WrappedJDBCType(jpype_dbapi2.LONGVARCHAR, str)
Longvarbinary = WrappedJDBCType(jpype_dbapi2.LONGVARBINARY, bytes)
Longvarchar = WrappedJDBCType(jpype_dbapi2.LONGVARCHAR, str)
Nchar = WrappedJDBCType(jpype_dbapi2.NCHAR, str)
Nclob = WrappedJDBCType(jpype_dbapi2.NCLOB, str)
Null: WrappedJDBCType[JDBCType, None] = WrappedJDBCType(jpype_dbapi2.NULL, type(None))
Numeric = WrappedJDBCType(jpype_dbapi2.NUMERIC, _Decimal)
Nvarchar = WrappedJDBCType(jpype_dbapi2.NVARCHAR, str)
Other = WrappedJDBCType(jpype_dbapi2.OTHER, object)
Real = WrappedJDBCType(jpype_dbapi2.REAL, float)
Ref = WrappedJDBCType(jpype_dbapi2.REF, object)
Rowid = WrappedJDBCType(jpype_dbapi2.ROWID, object)
Resultset = WrappedJDBCType(jpype_dbapi2.RESULTSET, object)
Smallint = WrappedJDBCType(jpype_dbapi2.SMALLINT, int)
Sqlxml = WrappedJDBCType(jpype_dbapi2.SQLXML, str)
Time = WrappedJDBCType(jpype_dbapi2.TIME, time)
Time_with_timezone = WrappedJDBCType(jpype_dbapi2.TIME_WITH_TIMEZONE, time)
Timestamp = WrappedJDBCType(jpype_dbapi2.TIMESTAMP, datetime)
Timestamp_with_timezone = WrappedJDBCType(
    jpype_dbapi2.TIMESTAMP_WITH_TIMEZONE, datetime
)
Tinyint = WrappedJDBCType(jpype_dbapi2.TINYINT, int)
Varbinary = WrappedJDBCType(jpype_dbapi2.VARBINARY, bytes)
Varchar = WrappedJDBCType(jpype_dbapi2.VARCHAR, str)
# alias
String = WrappedJDBCType(jpype_dbapi2.STRING, str)
Text = WrappedJDBCType(jpype_dbapi2.TEXT, str)
Binary = WrappedJDBCType(jpype_dbapi2.BINARY, bytes)
Number = WrappedJDBCType(jpype_dbapi2.NUMBER, int)
Float = WrappedJDBCType(jpype_dbapi2.FLOAT, float)
Decimal = WrappedJDBCType(jpype_dbapi2.DECIMAL, _Decimal)
Datetime = WrappedJDBCType(jpype_dbapi2.TIMESTAMP, datetime)
# special
Ascii_stream = WrappedJDBCType(jpype_dbapi2.ASCII_STREAM, str)
Binary_stream = WrappedJDBCType(jpype_dbapi2.BINARY_STREAM, bytes)
Character_stream = WrappedJDBCType(jpype_dbapi2.CHARACTER_STREAM, str)
Ncharacter_stream = WrappedJDBCType(jpype_dbapi2.NCHARACTER_STREAM, str)
Url = WrappedJDBCType(jpype_dbapi2.URL, str)
# sqlalchemy
_QuotedName = JDBCType(
    "quoted_name", String.type_code, getter=String.getter, setter=String.setter
)
QuotedName = WrappedJDBCType(_QuotedName, quoted_name)
### declare:: end

_time_codes = frozenset(
    x.type_code for x in (Time, Time_with_timezone) if x.type_code is not None
)
_time_names = frozenset(
    x.name.upper() for x in (Time, Time_with_timezone) if x.name is not None
)
_date_codes = frozenset(x.type_code for x in (Date,) if x.type_code is not None)
_date_names = frozenset(x.name.upper() for x in (Date,) if x.name is not None)
_datetime_codes = frozenset(
    x.type_code for x in (Timestamp, Timestamp_with_timezone) if x.type_code is not None
)
_datetime_names = frozenset(
    chain(
        (
            x.name.upper()
            for x in (Timestamp, Timestamp_with_timezone)
            if x.name is not None
        ),
        ("DATETIME",),
    )
)
_date_all_codes = frozenset(chain(_time_codes, _date_codes, _datetime_codes))
_date_all_names = frozenset(chain(_time_names, _date_names, _datetime_names))
_date_types = frozenset((datetime, date, time))


def find_type_code(description: Description | int | str | None) -> int | None:
    if isinstance(description, tuple):
        description = description[1]

    if isinstance(description, int):
        return description

    if not description:
        return None

    return TypeCodes.get(description, None)


def get_wrapped_type(jdbc_type: JDBCType) -> WrappedJDBCType[JDBCType, Any]:
    return _registry[jdbc_type]


class ParseStringToTime:
    def __init__(self, type_code: int, type_name: str) -> None:
        self._type_code = type_code
        self._type_name = type_name

    def get(self, rs: ResultSet, column: int, st: bool) -> Any:  # noqa: FBT001, PLR0911
        value = String.get(rs, column, st)
        value = str(value)
        if value.isdigit():
            value = float(value) / 1000

        if self._type_name in _datetime_names or self._type_code in _datetime_codes:
            if isinstance(value, str):
                return datetime.fromisoformat(value)
            return datetime.fromtimestamp(value)  # noqa: DTZ006
        if self._type_name in _date_names or self._type_code in _date_codes:
            if isinstance(value, str):
                return date.fromisoformat(value)
            return date.fromtimestamp(value)  # noqa: DTZ012
        if self._type_name in _time_names or self._type_code in _time_codes:
            if isinstance(value, str):
                return time.fromisoformat(value)
            return datetime.fromtimestamp(value).time()  # noqa: DTZ006
        return value

    def set(self, ps: Any, column: int, value: Any) -> Any:
        if isinstance(value, DateStr):
            dtype = value._dtype  # noqa: SLF001
            value = value._date  # noqa: SLF001
            return jpype_dbapi2._default_setters[dtype].set(ps, column, value)  # noqa: SLF001

        value = str(value)
        if self._type_name in _datetime_names or self._type_code in _datetime_codes:
            value = datetime.fromisoformat(value)
            return Timestamp.set(ps, column, value)
        if self._type_name in _date_names or self._type_code in _date_codes:
            value = date.fromisoformat(value)
            return Date.set(ps, column, value)
        if self._type_name in _time_names or self._type_code in _time_codes:
            value = time.fromisoformat(value)
            return Time.set(ps, column, value)

        error_msg = f"Unknown type: {self._type_name}"
        raise TypeError(error_msg)


class DateStrSetter:
    @staticmethod
    def set(ps: Any, column: int, value: DateStr[Any]) -> Any:
        dtype = value._dtype  # noqa: SLF001
        dvalue = value._date  # noqa: SLF001
        return jpype_dbapi2._default_setters[dtype].set(ps, column, dvalue)  # noqa: SLF001


class UseDsn:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def getter(self, cx: jpype_dbapi2.Connection, meta: _JDBCMeta, index: int) -> Any:
        if "sqlite" in self._dsn:
            type_name = meta.getColumnTypeName(index + 1)
            type_code = meta.getColumnType(index + 1)
            if type_name in _date_all_names or type_code in _date_all_names:
                return ParseStringToTime(type_code, type_name)
        return jpype_dbapi2.GETTERS_BY_NAME(cx, meta, index)

    def setter(
        self,
        cx: jpype_dbapi2.Connection,
        meta: _JDBCMeta,
        index: int,
        python_type: type[Any],
    ) -> Any:
        if "sqlite" in self._dsn or "postgres" in self._dsn:
            try:
                type_code = meta.getParameterType(index + 1)
                type_name = str(meta.getParameterTypeName(index + 1)).upper()
            except (Error, jpype_dbapi2.Error):
                if python_type in _date_types:
                    return String
            else:
                if type_name in _date_all_names or type_code in _date_all_names:
                    return ParseStringToTime(type_code, type_name)

        return jpype_dbapi2.SETTERS_BY_TYPE(cx, meta, index, python_type)


def _init_types() -> None:
    try:
        import sqlalchemy as sa
    except ImportError:  # pragma: no cover
        return

    jpype_dbapi2._default_setters[sa.quoted_name] = _QuotedName  # noqa: SLF001
    jpype_dbapi2._default_setters[DateStr] = DateStrSetter  # noqa: SLF001


jpype._jinit.registerJVMInitializer(_init_types)  # noqa: SLF001
