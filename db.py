from pymongo import MongoClient

class Database():

    IP = "localhost"
    PORT = 27017
    DATABASE = "colibri_db"

    def connect_mongo(self):
        connection = MongoClient(self.IP, self.PORT)
        return connection

    def disconnect_mongo(self, connection):
        connection.disconnect()

    def get_collection(self, connection, collection):
        db = connection[self.DATABASE]
        return list(db[collection].find({},{'_id': 0}))
