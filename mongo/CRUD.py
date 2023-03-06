import pymongo
import uuid

client = pymongo.MongoClient('mongodb+srv://noticy:3tU69hDdOCBXUWcp@cluster0.mlaq4tt.mongodb.net/?retryWrites=true&w=majority')

try:
    client.admin.command('ping')
except pymongo.erros.ConnectionFailure:
    print("Server not available")

print('Databases:')
for db_info in client.list_database_names():
   print(db_info)

db = client['odl']

collections = db.list_collection_names()

print("Collections:")
for collection in collections:
   print(collection)

posts = db['post']
# posts.insert_one(document={"_id":str(uuid.uuid4()), 'title':'dasd'},)
posts.delete_many({'title':'dasd'})


