# ud-database-project

To run this, open the PostgreSQL CLI (psql) and run the following
command to create 3 helper views:

```
create view slugs_accessed as
select split_part(path, '/', 3) as slug from log
where log.path LIKE '/article/%'
and status = '200 OK';

create view total as
select time::date as day, count(*) as c
from log group by day;

create view error as
select time::date as day, count(*) as c
from log where status != '200 OK' group by day;
```

Then, just run the main script:

```
python main.py
```

If you need to install dependencies, run:

```
pip install -r requirements.txt
```