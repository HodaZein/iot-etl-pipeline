"""load: write to sqlite warehouse."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "out" / "warehouse.db"
SCHEMA = ROOT / "sql" / "schema.sql"


def load(machines: pd.DataFrame, readings: pd.DataFrame, db: Path = DB) -> int:
    db.parent.mkdir(parents=True, exist_ok=True)
    db.unlink(missing_ok=True)
    with sqlite3.connect(db) as con:
        con.executescript(SCHEMA.read_text())
        machines.to_sql("dim_machine", con, if_exists="append", index=False)
        readings[["machine_id", "ts", "metric", "value"]].to_sql(
            "fact_reading", con, if_exists="append", index=False
        )
        rows = con.execute("select count(*) from fact_reading").fetchone()[0]
    return rows
