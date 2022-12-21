import pytest
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

import shark
from shark.testing import yield_sqlite_test_resources
from shark.tickers.sql import _SQL_DB_PATH


@pytest.fixture
def resources() -> tuple[Engine, MetaData]:
    yield from yield_sqlite_test_resources(
        _SQL_DB_PATH, creator=shark.tickers.sql.define_db
    )


def test_run(resources: tuple[Engine, MetaData]) -> None:
    engine, _ = resources
    tickers_to_inserts = shark.tickers.scrape.run(engine=engine)
    assert sum(tickers_to_inserts.values()) > 0
