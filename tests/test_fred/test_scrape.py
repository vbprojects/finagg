import pytest
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

import shark
from shark.fred.sql import _DATABASE_PATH


@pytest.fixture
def resources() -> tuple[Engine, MetaData]:
    yield from shark.testing.sqlite_resources(
        _DATABASE_PATH, creator=shark.yfinance.sql.define_db
    )


def test_run(resources: tuple[Engine, MetaData]) -> None:
    engine, _ = resources
    tickers_to_inserts = shark.fred.scrape.run(
        shark.fred.features.economic_features.series_ids, engine=engine
    )
    assert sum(tickers_to_inserts.values()) > 0
