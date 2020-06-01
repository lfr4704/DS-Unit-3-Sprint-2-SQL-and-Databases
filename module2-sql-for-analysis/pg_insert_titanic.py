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


#this creates a pandas df to a list of tuples
list_of_tuples= list(df.to_records(index=False))

insertion_query = f"INSERT INTO passengers (survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples) #third param: data as a list

#Queries for assignment 4

# How many passengers survived, and how many died?
# How many passengers were in each class?
# How many passengers survived/died within each class?
# What was the average age of survivors vs nonsurvivors?
# What was the average age of each passenger class?
# What was the average fare by passenger class? By survival?
# How many siblings/spouses aboard on average, by passenger class? By survival?
# How many parents/children aboard on average, by passenger class? By survival?
# Do any passengers have the same name?
# (Bonus! Hard, may require pulling and processing with Python) How many married couples were aboard the Titanic? Assume that two people (one Mr. and one Mrs.) with the same last name and with at least 1 sibling/spouse aboard are a married couple.



# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()
