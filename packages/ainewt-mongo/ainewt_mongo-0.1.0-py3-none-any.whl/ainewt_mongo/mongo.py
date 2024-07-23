import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self):
        self.mongodb_url = os.environ.get('API_MONGODB', 'mongodb://localhost:27017')
        self.database_name = os.environ.get('MONGODB_DATABASE', 'convert_pdf')
        self.coll_count_name = os.environ.get('MONGODB_COLLECTION_COUNT', 'count')
        self.coll_user_name = os.environ.get('MONGODB_COLLECTION_USER_LOG', 'user_log')
        self.coll_pdf_name = os.environ.get('MONGODB_COLLECTION_PDF_INFO', 'pdf_info')
        self.coll_page_name = os.environ.get('MONGODB_COLLECTION_PAGE_INFO', 'page_info')
        self.coll_tuning_name = os.environ.get('MONGODB_COLLECTION_TUNING_DATA', 'tuning_data')
        self.client = MongoClient(self.mongodb_url)
        self.db = self.client.get_database(self.database_name)
        self.coll_count = self.db.get_collection(self.coll_count_name)
        self.coll_user_log = self.db.get_collection(self.coll_user_name)
        self.coll_pdf_info = self.db.get_collection(self.coll_pdf_name)
        self.coll_page_info = self.db.get_collection(self.coll_page_name)
        self.coll_tuning_data = self.db.get_collection(self.coll_tuning_name)

    def find_count(self, file_name):
        doc = {'file_name': file_name}
        return self.coll_count.find_one(doc)

    def insert_count(self, file_name):
        doc = {
            'file_name': file_name,
            'count': 0,
            'log': ''
        }
        return self.coll_count.insert_one(doc)

    def update_count(self, file_name, text):
        doc = self.find_count(file_name)
        count = doc['count'] + 1
        log = text + '\n' + doc['log']
        self.coll_count.update_one({'file_name': file_name}, {'$set': {'count': count, 'log': log}})

    def insert_PDF_info(self, project: str, file_name: str, uuid: str, total_page: int, width: int, height: int):
        doc = {
            'project': project,
            'file_name': file_name,
            'uuid': uuid,
            'total_page': total_page,
            'width': width,
            'height': height,
            'upload_date': datetime.utcnow() + timedelta(hours=9)
        }
        return self.coll_pdf_info.insert_one(doc)

    def insert_page_info(self, pdf_info: str, page: int, table: List, text: List, figure: List):
        doc = {
            'pdf_info': pdf_info,
            'page': page,
            'table': table,
            'text': text,
            'figure': figure
        }
        return self.coll_page_info.insert_one(doc)

    def select_info(self, uuid: str):
        pipeline = [
            {"$match": {"uuid": uuid}},
            {"$lookup": {
                "from": "page_info",
                "localField": "_id",
                "foreignField": "pdf_info",
                "as": "page_info"
            }}
        ]
        return self.coll_pdf_info.aggregate(pipeline)

    def select_train_data(self, project: str):
        doc = {'project': project}
        return self.coll_tuning_data.find_one(doc)
