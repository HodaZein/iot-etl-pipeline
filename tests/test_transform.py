import pandas as pd
from etl import transform


def test_clean_drops_duplicates():
    df = pd.DataFrame(
        [
            {"machine_id": "M-1", "ts": "2026-01-01T00:00:00Z", "metric": "t", "value": 1.0},
            {"machine_id": "M-1", "ts": "2026-01-01T00:00:00Z", "metric": "t", "value": 1.0},
        ]
    )
    out = transform.clean_sensors(df)
    assert len(out) == 1


def test_clean_drops_null_values():
    df = pd.DataFrame(
        [
            {"machine_id": "M-1", "ts": "2026-01-01T00:00:00Z", "metric": "t", "value": None},
            {"machine_id": "M-1", "ts": "2026-01-01T00:05:00Z", "metric": "t", "value": 2.0},
        ]
    )
    out = transform.clean_sensors(df)
    assert len(out) == 1
    assert out.iloc[0]["value"] == 2.0


def test_clean_drops_unparseable_ts():
    df = pd.DataFrame(
        [
            {"machine_id": "M-1", "ts": "not-a-date", "metric": "t", "value": 1.0},
            {"machine_id": "M-1", "ts": "2026-01-01T00:05:00Z", "metric": "t", "value": 2.0},
        ]
    )
    out = transform.clean_sensors(df)
    assert len(out) == 1


def test_filter_unknown_machines():
    sensors = pd.DataFrame(
        [
            {"machine_id": "M-1", "ts": "2026-01-01T00:00:00Z", "metric": "t", "value": 1.0},
            {"machine_id": "M-XXX", "ts": "2026-01-01T00:00:00Z", "metric": "t", "value": 2.0},
        ]
    )
    machines = pd.DataFrame([{"machine_id": "M-1"}])
    out = transform.filter_known_machines(sensors, machines)
    assert list(out["machine_id"]) == ["M-1"]
