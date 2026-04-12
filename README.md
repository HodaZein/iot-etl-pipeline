# iot-etl-pipeline

small ETL pipeline I wrote on the side to play with IoT-sensor-style data. nothing from work, all synthetic.

idea: heterogeneous JSON sensor streams + a master CSV of machines -> cleaned sqlite warehouse you can query.

## what it does
1. read raw sensor JSON files from `sample_data/sensors/`
2. read master CSV `sample_data/machines.csv`
3. clean: parse timestamps, drop null values, drop dupes, drop readings for unknown machines
4. write to sqlite (`out/warehouse.db`) - one fact table + one dim

## stack
python 3.10+, pandas, pytest, sqlite

## run
```
pip install -r requirements.txt
python -m etl
pytest -q
```

## layout
- `etl/` pipeline (extract / transform / load)
- `tests/` pytest tests
- `sample_data/` small inputs (committed so it runs out of the box)
- `sql/` schema

## what I deliberately did not do
- no airflow / prefect, this is just a script
- no incremental load - full reload every run
- happy path + a few error cases tested, not exhaustive
