import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

# client = pymongo.MongoClient("mongodb://{DB_USER}:{DB_PASSWORD}@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin")
# db = client.test

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"
print("----------------")
print("URI:", connection_uri)

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)
print(dir(client))
print("DB NAMES:", client.list_database_names)

db = client.test_database # "test_database" or whatever you want to call it
print("----------------")
print("DB:", type(db), db)

collection = db.pokemon_collection # "pokemon_test" or whatever you want to call it
print("----------------")
print("COLLECTION:", type(collection), collection)

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())

collection.insert_one({
    "name": "Pikachu",
    "level": 30,
    "exp": 76000000000,
    "hp": 400,
    "fav_icecream_flavors": ["vanilla", "choc"],
    "stats": {"a": 1, "b": 2, "c": [1,2,3]}
})
print("DOCS:", collection.count_documents({})) # SELECT count(distinct id) FROM pokemon
print(collection.count_documents({"name": "Pikachu"})) #SELECT count(distinct id) from pokemon WHERE name = "Pikachu"

mewtwo = {
    "name": "Mewtwo",
    "level": 100,
    "exp": 76000000000,
    "hp": 450,
    "strength": 550,
    "intelligence": 450,
    "dexterity": 300,
    "wisdom": 575
}

pikachu = {
    "name": "Pikachu",
    "level": 30,
    "exp": 76000000000,
    "hp": 400,
}

blastoise = {
    "name": "Blastoise",
    "lvl": 70,
}

pokemon_team = [mewtwo, pikachu, blastoise]
collection.insert_many(pokemon_team)

print("DOCS:", collection.count_documents({})) # SELECT count(distinct id) FROM pokemon


pikas = list(collection.find({"name": "Pikachu"})) # SELECT * FROM pokemon WHERE name = "Pikachu"
print(len(pikas), "PIKAS")

print(pikas[0]["_id"])
print(pikas[0]["name"])


strong = list(collection.find({'level': {'$gte': 10}}))
print("Strong", len(strong))
# print("INSERT ONE AT A TIME...")
# for character in characters:
#     print(character["name"])
#     collection.insert_one(character)
#
# print(collection.count_documents({}), "DOCS")
# print(collection.count_documents({"level": {"$gte": 50}}), "ABOVE 50")
# print(collection.count_documents({"name": "Pikachu"}))

# print("INSERT MANY...")
#
# db.things.insert_one({"thing":"one"})
# db.things.insert_many([{"thing":"one"}, {"thing": "two"}])
# print(db.things.count_documents({"thing": "one"}))
