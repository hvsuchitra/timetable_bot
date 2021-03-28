"""
This is a script that is used to populate an empty MySQL DB in AWS RDS
for use with the chat bot in AWS Lex which invokes the AWS Lambda function.
"""

from random import shuffle
from itertools import product

import pymysql

days = range(1, 8)  # Monday 1 to Sunday 7
timings = range(1, 7)  # First 1 to Sixth 6
staff = range(1, 3)  # 1, 2
periods = range(1, 6)  # 1 to 5

res = list(product(days, timings, staff, periods))  # Create a Cartesian product of the above values

shuffle(res)  # Shuffle before extracting random 42 values

seen = set()

random_time_table = []  # this list will hold randomly selected unique values, used to populate the "timetable" table

for day, timing, staff, period in res:
    if (day, timing) in seen:  # skip if (day, timing) pair is already added
        continue
    seen.add((day, timing))
    random_time_table.append((day, timing, staff, period))

assert len(random_time_table) == 42, 'Exactly 42 slots were not filled'  # 7 days * 6 periods = 42

# create queries

c_period = '''create table if not exists periods (
    id  integer,
    period  varchar(255),
    primary key(id)
)'''

c_days = '''create table if not exists days (
    id  integer,
    day varchar(255) not null,
    primary key(id)
)'''

c_staff = '''create table if not exists staff (
    id  integer,
    staff_name  varchar(255) not null,
    primary key(id)
)'''

c_timings = '''create table if not exists timings (
    id  integer,
    timing  varchar(255) not null,
    primary key(id)
)'''

c_timetable = '''create table if not exists timetable (
    day_id  integer,
    timing_id   integer,
    staff_id    integer,
    period_id   integer,
    foreign key(staff_id) references staff(id),
    foreign key(period_id) references periods(id),
    primary key(day_id,timing_id),
    foreign key(day_id) references days(id),
    foreign key(timing_id) references timings(id)
)'''

create_queries = c_period, c_days, c_staff, c_timings, c_timetable

# insert queries

i_periods = '''insert into periods values
(1 , 'Language'),
(2 , 'English'),
(3 , 'Maths'),
(4 , 'Social'),
(5 , 'Science')'''

i_days = '''insert into days values
(1, 'Monday'),
(2, 'Tuesday'),
(3, 'Wednesday'),
(4, 'Thursday'),
(5, 'Friday'),
(6, 'Saturday'),
(7, 'Sunday')'''

i_staff = '''insert into staff values
(1, 'S'),
(2, 'G')'''

i_timings = '''insert into timings values
(1, 'First'),
(2, 'Second'),
(3, 'Third'),
(4, 'Fourth'),
(5, 'Fifth'),
(6, 'Sixth')'''

i_timetable = 'insert into timetable values (%s, %s, %s, %s)' # template for parameterization

insert_queries = i_periods, i_days, i_staff, i_timings

queries = create_queries, insert_queries

connection_parameters = {'host': 'my_database_endpoint_at_region.rds.amazonaws.com', 'user': 'user_name',
                         'password': 'password_given', 'database': 'database_name'}

with pymysql.connect(**connection_parameters) as conn, conn.cursor() as cur:
    for query_group in queries:
        for query in query_group:
            cur.execute(query)
    cur.executemany(i_timetable, random_time_table)
    conn.commit()
