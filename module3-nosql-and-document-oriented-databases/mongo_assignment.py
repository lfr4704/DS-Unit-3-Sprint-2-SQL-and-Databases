import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

client = pymongo.MongoClient("mongodb://<USERNAME>:<PASSWORD>@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin")
db = client.test

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"
print("----------------")
print("URI:", connection_uri)

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)

db = client.test_database # "test_database" or whatever you want to call it
print("----------------")
print("DB:", type(db), db)

collection = db.pokemon_test # "pokemon_test" or whatever you want to call it
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
})
print("DOCS:", collection.count_documents({}))
print(collection.count_documents({"name": "Pikachu"}))
