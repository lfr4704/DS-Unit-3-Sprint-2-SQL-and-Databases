import os
from dotenv import load_dotenv
import psycopg2

load_dotenv() #> loads contents of the .env file into the script's environment

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

# create a table to store the passengers
query = """
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived bool,
    pclass int,
    name varchar,
    sex varchar,
    age int,
    sib_spouse_count int,
    parent_child_count int,
    fare float8
);
"""

cursor.execute(query)

connection.commit() # actually update the database

# TODO: read CSV contents and insert rows into a new table
