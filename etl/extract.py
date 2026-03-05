"""extract: read raw inputs from disk."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SENSOR_DIR = ROOT / "sample_data" / "sensors"
MACHINES = ROOT / "sample_data" / "machines.csv"


def read_machines(path: Path = MACHINES) -> pd.DataFrame:
    return pd.read_csv(path)


def read_sensors(folder: Path = SENSOR_DIR) -> pd.DataFrame:
    frames = []
    for fp in sorted(folder.glob("*.json")):
        data = json.loads(fp.read_text())
        df = pd.DataFrame(data)
        df["_source"] = fp.name
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["machine_id", "ts", "metric", "value", "_source"])
    return pd.concat(frames, ignore_index=True)
