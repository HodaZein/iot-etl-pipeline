drop table if exists dim_machine;
create table dim_machine (
    machine_id text primary key,
    plant text not null,
    line text not null,
    commissioned text not null
);

drop table if exists fact_reading;
create table fact_reading (
    machine_id text not null,
    ts text not null,
    metric text not null,
    value real,
    foreign key (machine_id) references dim_machine(machine_id)
);

create index idx_fact_machine on fact_reading(machine_id);
create index idx_fact_ts on fact_reading(ts);
create index idx_fact_metric on fact_reading(metric);
