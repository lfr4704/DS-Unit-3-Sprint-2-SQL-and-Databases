import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from psycopg2.extras import execute_values
import json
import pandas as pd

load_dotenv() # reads the contents of the .env file and adds them to the environment

DB_NAME = os.getenv("DB_NAME", default="OOOPs")
DB_USER = os.getenv("DB_USER", default="OOOPs")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOOPs")
DB_HOST = os.getenv("DB_HOST", default="OOOPs")

### Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST)

print("CONNECTION", type(connection))
### A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor(cursor_factory=DictCursor)
print('CURSOR', type(cursor))
### An example query
cursor.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
#result = cur.fetchone()
result = cursor.fetchall()

for row in result:
    print("_____")
    print(type(row))
    print(row)


#
# CREATE THE TABLE
#

table_name = "test_table2"

print("-------------------")
query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  data JSONB
);
"""
print("SQL:", query)
cursor.execute(query)

#
# INSERT SOME DATA
#

my_dict = { "a": 1, "b": ["dog", "cat", 42], "c": 'true' }

# insertion_query = f"INSERT INTO test_table2 (name, data) VALUES (%s, %s)"
# cursor.execute(insertion_query,
#  ('A rowwwww', 'null')
# )
# cursor.execute(insertion_query,
#  ('Another row, with JSONNNNN', json.dumps(my_dict))
# )

# h/t: https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
insertion_query = f"INSERT INTO test_table2 (name, data) VALUES %s"
execute_values(cursor, insertion_query, [
 ('A rowwwww', 'null'),
 ('Another row, with JSONNNNN', json.dumps(my_dict)),
 ('Third row', "3")
])

df = pd.DataFrame([
  ['A rowwwww', 'null'],
  ['Another row, with JSONNNNN', json.dumps(my_dict)],
  ['Third row', "null"],
  ["Pandas Row", "null"]
])

records = df.to_dict("records") #> [{0: 'A rowwwww', 1: 'null'}, {0: 'Another row, with JSONNNNN', 1: '{"a": 1, "b": ["dog", "cat", 42], "c": "true"}'}, {0: 'Third row', 1: '3'}, {0: 'Pandas Row', 1: 'YOOO!'}]
list_of_tuples = [(r[0], r[1]) for r in records]

execute_values(cursor, insertion_query, list_of_tuples)

#
# QUERY THE TABLE
#

print("-------------------")
query = f"SELECT * FROM test_table2;"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()
