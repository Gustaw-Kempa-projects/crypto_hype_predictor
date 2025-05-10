
    
    create view main."mavg_data" as
    

with source as (
  select *
  from main."final_data"
),
mavgs as (
  select
    t1.date,
    t1.name,
    t1.name_hype,
    (
      select avg(t2.name_hype)
      from source t2
      where
        t2.name = t1.name and
        t2.date <= t1.date and
        t2.date >= datetime(t1.date, '-7 days')
    ) as mavg_name,
    (
      select
        sqrt(avg(t2.name_hype * t2.name_hype) - avg(t2.name_hype) * avg(t2.name_hype))
      from source t2
      where
        t2.name = t1.name and
        t2.date <= t1.date and
        t2.date >= datetime(t1.date, '-7 days')
    ) as stddev_name
  from source t1
)
select * from mavgs;