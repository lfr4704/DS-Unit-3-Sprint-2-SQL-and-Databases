import os
import sqlite3
import psycopg2
import numpy as np
from psycopg2.extras import execute_values

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

#Part 1
# construct a path to wherever your database exists

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "SC", "demo_data.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)

print("CONNECTION:", connection)
#connection.row_factory = sqlite3.Row
cursor = connection.cursor()
print("CURSOR", cursor)

# create a table to store the passenger
drop_existing_sql_table = """
DROP TABLE IF EXISTS demo_data;
"""

table_creation_sql = """
CREATE TABLE IF NOT EXISTS demo_data (
    id SERIAL PRIMARY KEY,
    "s" text,
    "x" int4,
    "y" int4);
"""

insertion_query1 = """

INSERT INTO demo_data (
    s,
    x,
    y)
VALUES (
    'g',
    3,
    9);
"""

insertion_query2 = """

INSERT INTO demo_data (
    s,
    x,
    y)
VALUES (
    'v',
    5,
    7);
"""

insertion_query3 = """

INSERT INTO demo_data (
    s,
    x,
    y)
VALUES (
    'f',
    8,
    7);
"""

cursor.execute(drop_existing_sql_table)
cursor.execute(table_creation_sql)
cursor.execute(insertion_query1)
cursor.execute(insertion_query2)
cursor.execute(insertion_query3)


#- Count how many rows you have - it should be 3!
query = """
SELECT count(*)
FROM demo_data
"""

#- How many rows are there where both `x` and `y` are at least 5?
query2 = """
SELECT *
FROM demo_data
WHERE x = 5 AND y = 5
"""

#- How many unique values of `y` are there (hint - `COUNT()` can accept a keyword `DISTINCT`)?
query3 = """
SELECT COUNT(DISTINCT y)
FROM demo_data
"""


result = cursor.execute(query).fetchall()
result2 = cursor.execute(query2).fetchall()
result3 = cursor.execute(query3).fetchall()


print("RESULT 1:", result)
print("RESULT 2:", result2)
print("RESULT 3:", result3)


# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()
