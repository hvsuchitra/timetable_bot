"""This script cleans the DB in the RDS instance"""

import pymysql

connection_parameters = {'host': 'my_database_endpoint_at_region.rds.amazonaws.com', 'user': 'user_name',
                         'password': 'password_given', 'database': 'database_name'}

with pymysql.connect(**connection_parameters) as conn, conn.cursor() as cur:
    cur.execute('drop table if exists timetable')
    cur.execute('drop table if exists periods')
    cur.execute('drop table if exists days')
    cur.execute('drop table if exists staff')
    cur.execute('drop table if exists timings')
