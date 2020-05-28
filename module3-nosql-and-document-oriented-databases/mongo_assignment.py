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

print("number of characters:")
print(client.rpg.charactercreator_character.count_documents({}))

# row_count = 'SELECT COUNT(*) FROM charactercreator_character'
# sl_curs.execute(row_count).fetchall()
#
# get_characters = 'SELECT * FROM charactercreator_character'
# characters = sl_curs.execute(get_characters).fetchall()
#
# sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall()
#
# # run the script multiple times without it giving an error
# drop_table = '''DROP TABLE charactercreator_character;'''
# sl_curs.execute(drop_table)
#
# create_character_table = """
# CREATE TABLE charactercreator_character (
#   character_id SERIAL PRIMARY KEY,
#   name VARCHAR(30),
#   level INT,
#   exp INT,
#   hp INT,
#   strength INT,
#   intelligence INT,
#   dexterity INT,
#   wisdom INT
# );
# """
#
# sl_curs.execute(create_character_table)
# sl_conn.commit()
#
# # Fill table with characters
# for character in characters:
#     insert_character = """
#     INSERT INTO charactercreator_character
#     (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
#     VALUES """ + str(character[1:]) + ";"
#     sl_curs.execute(insert_character)
#     sl_conn.commit()
#
# # Make character_table a document
#
# character_query = "SELECT * FROM charactercreator_character;"
# charactercreator_character = sl_curs.execute(character_query).fetchone()
# # Different variable name here to avoid confusion
# all_characters = sl_curs.execute(character_query).fetchall()
#
# first_character = all_characters[0]
#
#
# rpg_doc = {
#     'sql_key': all_characters[0],
#     'name': all_characters[1],
#     'level': all_characters[2],
#     'exp': all_characters[3],
#     'hp': all_characters[4],
#     'strenth': all_characters[5],
#     'intelligence': all_characters[6],
#     'dexterity': all_characters[7],
#     'wisdom': all_characters[8]
# }
#
# collection.insert_one(rpg_doc)
#
# list(collection.find(rpg_doc))
#
# print(all_characters)
