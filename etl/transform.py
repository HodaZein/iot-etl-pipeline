"""transform: clean + join."""
from __future__ import annotations

import pandas as pd


def clean_sensors(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    # parse ts to UTC, drop bad ones
    out["ts"] = pd.to_datetime(out["ts"], utc=True, errors="coerce")
    out = out.dropna(subset=["ts"])
    # keep numeric values only (drop nulls)
    out = out[out["value"].notna()]
    # drop exct duplicates
    out = out.drop_duplicates(subset=["machine_id", "ts", "metric"])
    # iso strings for sqlite
    out["ts"] = out["ts"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return out.reset_index(drop=True)


def filter_known_machines(sensors: pd.DataFrame, machines: pd.DataFrame) -> pd.DataFrame:
    """drop sensor rows whose machine_id is not in the master."""
    if sensors.empty:
        return sensors
    known = set(machines["machine_id"])
    return sensors[sensors["machine_id"].isin(known)].reset_index(drop=True)
