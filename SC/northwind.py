import os
import sqlite3

#Part 1
# construct a path to wherever your database exists

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "SC", "northwind_small.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)

print("CONNECTION:", connection)
#connection.row_factory = sqlite3.Row
cursor = connection.cursor()
print("CURSOR", cursor)

# - What are the ten most expensive items (per unit price) in the database?

query = """
SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10
"""


# - What is the average age of an employee at the time of their hiring? (Hint: a
#   lot of arithmetic works with dates.)


query2 = """
SELECT AVG(hiredate - birthDate)
from Employee
"""


# - (*Stretch*) How does the average age of employee at hire vary by city?
# query3 = """
#
# """

result = cursor.execute(query).fetchall()
result2 = cursor.execute(query2).fetchall()
#result3 = cursor.execute(query3).fetchall()

print("RESULT 1:", result)
print("RESULT 2:", result2)
# print("RESULT 3:", result3)


cursor.close()
connection.close()
