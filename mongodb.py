import pymongo
from app_log import log


class MongoDB:
    def __init__(self, url):
        """instance variable for the file"""
        log.info('create the instance variable for the file')
        self.url = url

        #mongodb connection
        try:
            self.client = pymongo.MongoClient(self.url)
        except Exception as e:
            log.error('Connection error occured', e)
            print('Connection error occured')
        else:
            print('Connection established')


    def create_database(self, database_name):
        """Data base is created"""
        log.error('Create database')

        #create database
        try:
            self.database = self.client[str(database_name)]
            log.error('Database successfully created')
        except Exception as e:
            log.error('Database creation error occured', e)
            print('Database creation error occured')
        else:
            log.info(f"{database_name} already exists! Please chose different name" )
            print('Database name already exist')


    def create_collection(self, collection_name):
        """Collection or table is created"""
        log.error('Create collection')
        
        #create collection/table
        try:
            self.collection = self.database[str(collection_name)]
            log.error('Collection created successfully')
        except Exception as e:
            log.error('Collection creation error occured', e)
            print('Collection creation error occured')
        else:
            log.info(f"{collection_name} already exists! Please chose different name" )
            print('Collection name already exists')


    def find(self):
        """find a particular set of data"""
        log.info("Fetch records from collection")
        return self.collection.find()


    def insert(self, record):
        """clean the dataset and insert data into mongodb database"""
        log.info('execute the mongodb insertion function')
        try:
            #insert data into collection
            if type(record) == dict:
                self.collection.insert_one(record)
                log.error('Record inserted successfully')
            elif type(record) == list:
                self.collection.insert_many(record)
                log.error('Record inserted successfully')
        except Exception as e:
            log.error('Insertion operation error occured', e)
            print('Insertion operation error occured')
        else:
            print('Insertion operation successfully completed')