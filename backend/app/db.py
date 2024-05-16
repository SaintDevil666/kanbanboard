from flask import g
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

def get_db():
    if 'db' not in g:
        client = MongoClient(MONGO_URI)
        g.db = client[DB_NAME]
    return g.db