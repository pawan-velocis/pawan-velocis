#!/usr/bin/python
import sys
import pymongo
from pymongo import MongoClient
rows = {}
row_list=[]
rows["Host IP"]=str(sys.argv[1])
rows["Running_Configuration"]=str(sys.argv[2:])
row_list.append(rows)
def insertrunningconf(resp_dict):
    print("insertrunningconf: ", resp_dict)
    try:
        myclient = MongoClient("mongodb://10.18.1.53:27017/")
        db = myclient["psirt"]
        try:
            Collection = db["Non_Dnac_Device_Running_Configure"]
        except pymongo.errors.CursorNotFound:
            print("Cursor Not Found")
    except pymongo.errors.ConnectionFailure:
        print("Could not connect to MongoDB")
    if isinstance(resp_dict, list):
        print('many*************')
        try:
            Collection.create_index('Host IP', unique = True)
            Collection.insert_many(resp_dict, ordered=False, bypass_document_validation=True)
        except pymongo.errors.BulkWriteError as e:
             print(e.details['writeErrors'])
    else:
        print('One*************')
        try:
            Collection.insert_one(resp_dict)
        except pymongo.errors.WriteError:
            print("Insertion Error")
insertrunningconf(row_list)
