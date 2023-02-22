from pymongo import MongoClient
from bson.json_util import dumps

class AnimalShelter(object):
    def __init__(self, username, password):
        self.client = MongoClient('mongodb://%s:%s@localhost:47040/AAC' % (username, password))
        self.database = self.client['AAC']
        try:
            x = dumps(self.database.animals.find_one())
        except:
            print("Failure")
            
    
# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            record = self.database.animals.insert_one(data)  # data should be dictionary  
            if record != 0:
                print("Animal has been added")
                return True
            else:
                print("Failed to add animal")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        
        
# Create method to implement the R in CRUD. 
    def read(self, searchKeyPair=None):
        # searchkeyPair is for example {id: 1} key/value
        if searchKeyPair:
            records = self.database.animals.find(searchKeyPair, {"_id": False})
        # searchKeyPair is none
        else:
            records = self.database.animals.find({},{"_id": False})
            
        return records
    
# Create method to implement the D in CRUD. 
    def update(self, index, update):
        # index is where we want to make changes
        # update is the update we want to make        
        if index != None and index != "" and update != None and update != "":
            update = {"$set": update}
            result = self.database.animals.update_many(index, update)
        else:
            raise Exception("Both index and update must not be empty.")
            
# Create method to implement the D in CRUD. 
    def delete(self, searchKeyPair):
        # searchkeyPair is for example {id: 1} key/value
        if searchKeyPair:
            result = self.database.animals.delete_many(searchKeyPair)
            print(result.deleted_count, " docs deleted")
        # searchKeyPair is none
        else:
            raise Exception("Specify which documents to delete.")
        
        
        
                                    
 