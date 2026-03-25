from pathlib import Path
from etl import extract


def test_read_machines():
    df = extract.read_machines()
    assert {"machine_id", "plant", "line", "commissioned"}.issubset(df.columns)
    assert len(df) > 0


def test_read_sensors_concats_files():
    df = extract.read_sensors()
    assert {"machine_id", "ts", "metric", "value"}.issubset(df.columns)
    # both sample files present
    assert df["_source"].nunique() >= 2
