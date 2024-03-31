import json
from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS
from model import TransactionModel

from fastapi.encoders import jsonable_encoder

class Database:
    def __init__(self) -> None:
        self.client = MongoClient(
            self.build_url()
        )
        self.database = self.client.get_database("dreyerxfaucet")
        
        self.transaction = self.database.get_collection("transactions")

    def build_url(self):
        uri = "mongodb://{}:{}/{}?authSource=admin".format(MONGO_HOST, MONGO_PORT, "dreyerxfaucet")
        return uri
    
    def save_transaction(self, transaction: TransactionModel):
        transaction_data    = jsonable_encoder(transaction)
        inserted_data      = self.transaction.insert_one(transaction_data)
        return transaction_data

    def transactions(self, limit):
        return self.transaction.find().sort("timestamp", -1).limit(limit=limit)