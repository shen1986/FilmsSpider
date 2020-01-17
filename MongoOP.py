from pymongo import MongoClient
client = MongoClient('xxxxxx', 27017) # 写上自己的MongoDB地址
db = client.films_database
filmCollection = db.newFilms