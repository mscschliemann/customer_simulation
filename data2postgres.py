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
 index |      timestamp      | customer_no | location | no_locations |              cust_path
-------+---------------------+-------------+----------+--------------+--------------------------------------
     0 | 2019-09-02 07:03:00 |           1 | da       |            2 | dach
     1 | 2019-09-02 07:03:00 |           2 | da       |            2 | dach
     2 | 2019-09-02 07:04:00 |           3 | da       |            2 | dach

           'week' Table Columns
 index |      timestamp      | customer_no | location | no_locations |              cust_path               |    day
-------+---------------------+-------------+----------+--------------+--------------------------------------+-----------
     0 | 2019-09-02 07:03:00 |           1 | da       |            2 | dach                                 | monday
     1 | 2019-09-02 07:03:00 |           2 | da       |            2 | dach                                 | monday
     2 | 2019-09-02 07:04:00 |           3 | da       |            2 | dach                                 | monday

"""


from sqlalchemy import create_engine
import psycopg2
import pandas as pd

engine = create_engine(...)

week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def replace_location_names(location):
    return location[0:2]

week_df = pd.DataFrame()
for day in week:
    df = pd.read_csv(day+'.csv', sep = ';')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['location'] = df['location'].apply(replace_location_names)
    loc_count_per_cust = pd.DataFrame(df.groupby('customer_no')['location'].count())
    cust_loc_path = pd.DataFrame(df.groupby('customer_no')['location'].sum())
    loc_count_per_cust.columns=['no_locations']
    cust_loc_path.columns=['cust_path']
    df = df.merge(loc_count_per_cust, how='left', left_on='customer_no', right_on='customer_no')
    df = df.merge(cust_loc_path, how='left', left_on='customer_no', right_on='customer_no')
    sql = f'DROP TABLE IF EXISTS "{day}";'
    engine.execute(sql)
    df.to_sql(day,engine)
    df['day'] = day
    week_df = pd.concat([week_df, df], ignore_index=True)
engine.execute('DROP TABLE IF EXISTS "week";')
week_df.to_sql('week', engine)
