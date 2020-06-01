"""
How was working with MongoDB different from working with PostgreSQL?
MongoDB allows you to use any programming language to make queries so working with python is convenient versus PostgreSQL uses SQL to make queries.
I found PostgreSQL and SQL to be harder.
"""

import sqlite3
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
#credentials
DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

# connect to pymongo
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority")
db = client.rpg # "test_database" or whatever you want to call it

#print(dir(client))
print("DB NAMES:", client.list_database_names)

collection = db.rpg_collection # "pokemon_test" or whatever you want to call it
print("----------------")
print("COLLECTION:", type(collection), collection)

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())

# Make rpg_db.sqlite3 character table
sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

# this is to run script multiple times and avoid errors
client.rpg.armory_item.drop()
client.rpg.armory_weapon.drop()
client.rpg.charactercreator_character.drop()

sl_curs.execute("""
    SELECT *
    FROM armory_item
""")
res = sl_curs.fetchall()
docs = [
    {
        "item_id": item_id,
        "name": name,
        "value": value,
        "weight": weight
    } for item_id, name, value, weight in res
]
client.rpg.armory_item.insert_many(docs)


sl_curs.execute("""
    SELECT *
    FROM armory_weapon
""")
res = sl_curs.fetchall()
docs = [
    {
        "item_ptr_id": item_ptr_id,
        "power": power
    } for item_ptr_id, power in res
]
client.rpg.armory_weapon.insert_many(docs)


sl_curs.execute("""
    SELECT *
    FROM charactercreator_character
""")
res = sl_curs.fetchall()
docs = [
    {
        "character_id": character_id,
        "name": name,
        "level": level,
        "exp": exp,
        "hp": hp,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "wisdom": wisdom,
    } for character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom in res
]
client.rpg.charactercreator_character.insert_many(docs)

# Queries
# How many total Characters are there?
print("number of characters:")
print(client.rpg.charactercreator_character.count_documents({}))
# How many total Items?
print("number of total items:")


#queries for assignment 4

# How many of each specific subclass?

# How many of the Items are weapons? How many are not?
# How many Items does each character have? (Return first 20 rows)
# How many Weapons does each character have? (Return first 20 rows)
# On average, how many Items does each Character have?
# On average, how many Weapons does each character have?
