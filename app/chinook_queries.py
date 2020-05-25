import os
import sqlite3

# construct a path to wherever your database exists

#DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "data", "chinook.db")
#DB_FILEPATH = "/Users/computer/projects/lambda/DS-Unit-3-Sprint-2-SQL-and-Databases/module1-introduction-to-sql/rpg_db.sqlite3"
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "data", "rpg_db.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)

print("CONNECTION:", connection)
#connection.row_factory = sqlite3.Row
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
#How many weapons does each chatarter have, print first 20

query3 ="""
    SELECT cci.character_id, COUNT(*)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    ) GROUP BY cci.character_id
    LIMIT 20;
"""

# -- How many Weapons does each character have?
# -- (Return first 20 rows)
# -- row per character (302, including ones that have zero)
# -- three cols: char id, char name, weapon_count
query4 = """
SELECT
  c.character_id
  ,c.name as character_name
  -- ,inv.item_id
  -- ,w.item_ptr_id as weapon_id
  ,count(distinct w.item_ptr_id) as weapon_count
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
LEFT JOIN armory_weapon w ON w.item_ptr_id = inv.item_id
GROUP BY 1
LIMIT 20
"""

#result = cursor.execute(query)
#print("RESULT", result) #> returns cursor object w/o results (need to fetch the results)

result2 = cursor.execute(query).fetchall()
result3 = cursor.execute(query2).fetchall()
result4 = cursor.execute(query3).fetchall()
result5 = cursor.execute(query4).fetchall()

# print("RESULT 2", dict(result2))
# print("RESULT 3", dict(result3))
# print("RESULT 4", result4[0][0])
# print("RESULT 5", result5[0][1])

print("RESULT 2", result2)
print("RESULT 3", result3)
print("RESULT 4", result4)
print("RESULT 5", result5)
