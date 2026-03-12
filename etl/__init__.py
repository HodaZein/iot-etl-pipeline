"""pipeline entry point."""
from __future__ import annotations

from . import extract, transform, load


def run() -> None:
    machines = extract.read_machines()
    sensors = extract.read_sensors()
    cleaned = transform.clean_sensors(sensors)
    filtered = transform.filter_known_machines(cleaned, machines)
    n = load.load(machines, filtered)
    print(f"loaded {n} readings into warehouse")


if __name__ == "__main__":
    run()
