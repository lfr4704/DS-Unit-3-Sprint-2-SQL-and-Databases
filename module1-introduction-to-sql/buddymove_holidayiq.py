import pandas as pd
import os
import sqlite3


# load database
csv_path = os.path.join(os.path.dirname(__file__), "..", "module1-introduction-to-sql", "buddymove_holidayiq.csv")
df = pd.read_csv(csv_path)
print(df)

# Open a connection to a new (blank) database file buddymove_holidayiq.sqlite3
connection = sqlite3.connect("buddymove_holidayiq.sqlite3")

# Use df.to_sql (documentation) to insert the data into a new table review in the SQLite3 database
df.to_sql("review", connection, if_exists='replace')
cursor = connection.cursor()

print("""
Count how many rows you have - it should be 249! """)
cursor.execute("""
    SELECT COUNT(*)
    FROM review
""")
print(cursor.fetchone())

print("""
How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?""")
cursor.execute("""
    SELECT COUNT(*)
    FROM review row
    WHERE row.Nature >= 100 AND row.Shopping >= 100
""")
print(cursor.fetchone())

print("""
(Stretch) What are the average number of reviews for each category? """)
cursor.execute("""
    SELECT AVG(Sports), AVG(Religious), AVG(Nature), AVG(Theatre), AVG(Shopping), AVG(Picnic)
    from review
""")
print(cursor.fetchone())
