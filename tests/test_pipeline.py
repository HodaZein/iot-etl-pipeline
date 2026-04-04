import sqlite3
from pathlib import Path

import pandas as pd
from etl import extract, transform, load


def test_end_to_end(tmp_path: Path):
    machines = extract.read_machines()
    sensors = extract.read_sensors()
    cleaned = transform.clean_sensors(sensors)
    filtered = transform.filter_known_machines(cleaned, machines)
    db = tmp_path / "test.db"
    n = load.load(machines, filtered, db=db)
    assert n > 0
    with sqlite3.connect(db) as con:
        rows = con.execute("select count(*) from dim_machine").fetchone()[0]
        assert rows == len(machines)
