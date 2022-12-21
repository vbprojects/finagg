"""Scrape the yfinance API for historical stock data and store into local SQL tables."""

from typing import Sequence

from sqlalchemy.engine import Engine

from . import api, sql


def run(
    tickers: str | Sequence[str],
    /,
    *,
    engine: Engine = sql.engine,
) -> dict[str, int]:
    """Scrape yfinance historical stock data from the
    yfinance API.

    ALL TABLES ARE DROPPED PRIOR TO SCRAPING!
    Scraped data is loaded into local yfinance SQL tables.

    Args:
        tickers: Company tickers to scrape.
        engine: Custom database engine to use.

    Returns:
        A dictionary mapping tickers to number of rows scraped
        for each ticker.

    """
    if isinstance(tickers, str):
        tickers = [tickers]

    sql.metadata.drop_all(engine)
    sql.metadata.create_all(engine)

    with engine.connect() as conn:
        tickers_to_inserts = {}
        for ticker in tickers:
            df = api.get(ticker, interval="1d", period="max")
            tickers_to_inserts[ticker] = len(df.index)
            conn.execute(sql.prices.insert(), df.to_dict(orient="records"))

    return tickers_to_inserts
