import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import numpy as np

load_dotenv() #> loads contents of the .env file into the script's environment

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

#read passenger data from the csv file
csv_path = os.path.join(os.path.dirname(__file__), "..", "module2-sql-for-analysis", "titanic.csv")
df = pd.read_csv(csv_path)
print(df)


#connec to pg database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)

# create a table to store the passenger
table_creation_sql = """
DROP TABLE IF EXISTS passengers;
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    "survived" int4,
    "pclass" int4,
    "name" text,
    "sex" text,
    "age" int4,
    "sib_spouse_count" int4,
    "parent_child_count" int4,
    "fare" float8
);
"""

cursor.execute(table_creation_sql)

# TODO: read CSV contents and insert rows into a new table

list_of_tuples= list(df.to_records(index=False))

insertion_query = f"INSERT INTO passengers (survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples) #third param: data as a list


# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()
