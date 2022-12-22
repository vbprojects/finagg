"""SQLAlchemy interfaces for mixed features."""

import os
import pathlib

from sqlalchemy import Column, MetaData, String, Table, create_engine, inspect
from sqlalchemy.engine import Engine, Inspector

_DATABASE_PATH = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "mixed_features.sqlite"
)

_DATABASE_URL = os.environ.get(
    "MIXED_FEATURES_DATABASE_URL",
    f"sqlite:///{_DATABASE_PATH}",
)


def define_db(
    url: str = _DATABASE_URL,
) -> tuple[tuple[Engine, MetaData], Inspector, tuple[Table, ...]]:
    """Utility method for defining the SQLAlchemy elements.

    Used for the main SQL tables and for creating test
    databases.

    Args:
        url: SQLAlchemy database URL.
        path: Path to database file.

    Returns:
        The engine, engine inspector, metadata, and tables associated with
        the database definition.

    """
    engine = create_engine(url)
    inspector: Inspector = inspect(engine)
    metadata = MetaData()
    if inspector.has_table("fundamental_features"):
        fundamental_features = Table(
            "fundamental_features",
            metadata,
            Column("ticker", String, primary_key=True, doc="Unique company ticker."),
            Column(
                "date", String, primary_key=True, doc="Filing and stock price dates."
            ),
            autoload_with=engine,
        )
    else:
        fundamental_features = None
    return (engine, metadata), inspector, (fundamental_features,)


(engine, metadata), inspector, (fundamental_features,) = define_db()
