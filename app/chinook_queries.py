import os
import sqlite3

# construct a path to wherever your database exists
#DB_FILEPATH = "chinook.db"
#DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "data", "chinook.db")
#DB_FILEPATH = "/Users/computer/projects/lambda/DS-Unit-3-Sprint-2-SQL-and-Databases/module1-introduction-to-sql/rpg_db.sqlite3"
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "data", "rpg_db.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)

print("CONNECTION:", connection)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
print("CURSOR", cursor)

#query = "SELECT * FROM charactercreator_character_inventory;"
#How many total Characters are there?
query = """
SELECT
	charactercreator_character.character_id,
	count(distinct charactercreator_character.character_id)
FROM
	charactercreator_character_inventory
INNER JOIN charactercreator_character ON charactercreator_character_inventory.character_id = charactercreator_character.character_id
"""
#How many total Items?
query2 = """
SELECT
	charactercreator_character.character_id,
	count(charactercreator_character.character_id)
FROM
	charactercreator_character_inventory
INNER JOIN charactercreator_character ON charactercreator_character_inventory.character_id = charactercreator_character.character_id
"""
#How many of the Items are weapons? How many are not?
query3 = """
SELECT
	charactercreator_character.character_id,
	count(charactercreator_character.character_id)
FROM
	charactercreator_character_inventory
INNER JOIN charactercreator_character ON charactercreator_character_inventory.character_id = charactercreator_character.character_id
"""

#result = cursor.execute(query)
#print("RESULT", result) #> returns cursor object w/o results (need to fetch the results)

result2 = cursor.execute(query).fetchall()
result3 = cursor.execute(query2).fetchall()
print("RESULT 2", dict(result2))
print("RESULT 3", dict(result3))
