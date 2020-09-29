"""
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | friday    | table | postgres
 public | monday    | table | postgres
 public | thursday  | table | postgres
 public | tuesday   | table | postgres
 public | wednesday | table | postgres
 public | week      | table | postgres

           <day> Tables Columns
  index |      timestamp      | customer_no | location
-------+---------------------+-------------+----------
     0 | 2019-09-02 07:03:00 |           1 | dairy
     1 | 2019-09-02 07:03:00 |           2 | dairy
     2 | 2019-09-02 07:04:00 |           3 | dairy

           'week' Table Columns
 index |      timestamp      | customer_no | location |    day
-------+---------------------+-------------+----------+-----------
     0 | 2019-09-02 07:03:00 |           1 | dairy    | monday
     1 | 2019-09-02 07:03:00 |           2 | dairy    | monday
     2 | 2019-09-02 07:04:00 |           3 | dairy    | monday

"""


from sqlalchemy import create_engine
import psycopg2
import pandas as pd

engine = create_engine(CONNECTION_STRING)

week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

week_df = pd.DataFrame()
for day in week:
    df = pd.read_csv(day+'.csv', sep = ';')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    sql = f'DROP TABLE IF EXISTS "{day}";'
    engine.execute(sql)
    df.to_sql(day,engine)
    df['day'] = day
    week_df = pd.concat([week_df, df], ignore_index=True)

engine.execute('DROP TABLE IF EXISTS "week";')
week_df.to_sql('week', engine)
