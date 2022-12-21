"""SEC SQLAlchemy interfaces."""

import os
import pathlib

from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    inspect,
)
from sqlalchemy.engine import Engine, Inspector

_SQL_DB_PATH = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent / "data" / "sec.sqlite"
)

_SQL_DB_URL = os.environ.get(
    "SEC_SQL_DB_URL",
    f"sqlite:///{_SQL_DB_PATH}",
)


def define_db(
    url: str = _SQL_DB_URL,
) -> tuple[tuple[Engine, MetaData], Inspector, tuple[Table, ...]]:
    """Utility method for defining the SQLAlchemy elements.

    Used for the main SQL tables and for creating test
    databases.

    Args:
        url: SQLAlchemy database URL.

    Returns:
        The engine, engine inspector, metadata, and tables associated with
        the database definition.

    """
    engine = create_engine(url)
    inspector: Inspector = inspect(engine)
    metadata = MetaData()
    submissions = Table(
        "submissions",
        metadata,
        Column("cik", String, primary_key=True, doc="Unique SEC ID."),
        Column(
            "entity_type", String, doc="Type of company standing (e.g., operating)."
        ),
        Column("sic", String, doc="Industry code."),
        Column("sic_description", String, doc="Industry code description."),
        Column(
            "insider_transaction_for_owner_exists",
            Integer,
            doc="Whether owner insider transactions data exists.",
        ),
        Column(
            "insider_transaction_for_issuer_exists",
            Integer,
            doc="Whether issuer insider transactions data exists.",
        ),
        Column("name", String, doc="Company name."),
        Column(
            "tickers", String, doc="Comma-separated tickers/symbols the company uses."
        ),
        Column(
            "exchanges",
            String,
            doc="Comma-separated exchanges the company is found on.",
        ),
        Column("ein", String, doc="Entity identification number."),
        Column("description", String, doc="Entity description (often empty/null)."),
        Column("website", String, doc="Company website (often empty/null)."),
        Column("investor_website", String, doc="Investor website (often empty/null)."),
        Column("category", String, doc="SEC entity category."),
        Column(
            "fiscal_year_end",
            String,
            doc="The company's last day of the fiscal year (MMDD).",
        ),
        Column("state_of_incorporation", String, doc="Official incorporation state."),
        Column(
            "state_of_incorporation_description",
            String,
            doc="State of incorporation description.",
        ),
    )

    tags = Table(
        "tags",
        metadata,
        Column("cik", String, doc="Unique SEC ID."),
        Column(
            "accn", String, primary_key=True, doc="Unique submission/access number."
        ),
        Column(
            "taxonomy", String, doc="XBRL taxonomy the submission's tag belongs to."
        ),
        Column(
            "tag",
            String,
            primary_key=True,
            doc="XBRL submission tag (e.g., NetIncomeLoss).",
        ),
        Column("form", String, doc="Submission form type (e.g., 10-Q)."),
        Column(
            "units",
            String,
            doc="Unit of measurements for tag value (e.g., USD or shares).",
        ),
        Column("fy", Integer, doc="Fiscal year the submission is for."),
        Column(
            "fp", String, doc="Fiscal period the submission is for (e.g., Q1 or FY)."
        ),
        Column(
            "start",
            String,
            nullable=True,
            doc="When the tag's value's measurements started.",
        ),
        Column("end", String, doc="When the tag's value's measurements ended."),
        Column("filed", String, doc="When the submission was actually filed."),
        Column(
            "frame",
            String,
            nullable=True,
            doc="Often a concatenation of `fy` and `fp`.",
        ),
        Column(
            "label", String, nullable=True, doc="More human readable version of `tag`."
        ),
        Column(
            "description",
            String,
            nullable=True,
            doc="Long description of `tag` and `label`.",
        ),
        Column("entity", String, doc="Company name."),
        Column("value", Float, doc="Tag value with units `units`."),
    )
    return (engine, metadata), inspector, (submissions, tags)


(engine, metadata), inspector, (submissions, tags) = define_db()
