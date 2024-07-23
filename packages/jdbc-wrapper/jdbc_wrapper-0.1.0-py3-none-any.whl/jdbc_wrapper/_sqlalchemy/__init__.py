from __future__ import annotations


def register_in_sqlalchemy() -> None:
    from sqlalchemy.dialects import registry

    registry.register(
        "postgresql.jdbc_wrapper",
        "jdbc_wrapper._sqlalchemy.postgresql",
        "PGJDBCDialect",
    )
    registry.register(
        "postgresql.jdbc_async_wrapper",
        "jdbc_wrapper._sqlalchemy.postgresql",
        "AsyncPGJDBCDialect",
    )
    registry.register(
        "mssql.jdbc_wrapper", "jdbc_wrapper._sqlalchemy.mssql", "MSJDBCDialect"
    )
    registry.register(
        "mssql.jdbc_async_wrapper",
        "jdbc_wrapper._sqlalchemy.mssql",
        "AsyncMSJDBCDialect",
    )
    registry.register(
        "sqlite.jdbc_wrapper", "jdbc_wrapper._sqlalchemy.sqlite", "SQJDBCDialect"
    )
    registry.register(
        "sqlite.jdbc_async_wrapper",
        "jdbc_wrapper._sqlalchemy.sqlite",
        "AsyncSQJDBCDialect",
    )
