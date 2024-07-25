import os
from trino.dbapi import connect as connect_to_trino  # type: ignore


def connect(
    host: str = "host.docker.internal",
    port: int = int(os.environ.get("TRINO_HOST_PORT", 8080)),
    user: str = os.environ.get("TRINO_USER", "trino"),
    catalog: str = "iceberg",
    schema: str = "raw",
):
    return connect_to_trino(
        host=host,
        port=port,
        user=user,
        catalog=catalog,
        schema=schema,
    )
