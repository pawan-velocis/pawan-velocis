#!/usr/bin/env python3.9
'''
custom dynamic inventory script for Ansible, in Python.
'''
import os
import sys
from bson import json_util
import argparse
from pymongo import MongoClient
import csv
try:
    import json
except ImportError:
    import simplejson as json
class ExampleInventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        self.viewcustom_template()
        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()
        print(json.dumps(self.inventory));

    def viewcustom_template(self):
        try:
            myclient = MongoClient("mongodb://10.18.1.53:27017/")
            db = myclient["psirt"]
            try:
                Collection = db["Non_DNAC_ANSIBLE"]
            except pymongo.errors.CursorNotFound:
                print("Cursor Not Found")
        except pymongo.errors.ConnectionFailure:
            print("Could not connect to MongoDB")
        y = []
        try:
            for x in Collection.find():
                y.append(x)
            y = json.loads(json_util.dumps(y))
        except pymongo.errors.PyMongoError:
            print("Mondodb find error")
        return y

    def example_inventory(self):
    # Converting MongoDB table to dictionary
            rows = {}
            new_data_dict = {}
            data = self.viewcustom_template()
            for row in data:
                item = dict()
                temp_list = []
                temp_list = row["hosts"].split(",")
                item["hosts"] = temp_list
                item["vars"] = dict()
                item["vars"]["ansible_ssh_user"] = row["ansible_ssh_user"]
                item["vars"]["ansible_ssh_pass"] =  row["ansible_ssh_pass"]
                item["vars"]["ansible_network_os"] =  row["ansible_network_os"]
                item["vars"]["ansible_python_interpreter"] =  row["ansible_python_interpreter"]
                new_data_dict[row["Groups"]] = item
                item = {}
                item['hostvars'] = {}
                new_data_dict[row["_meta"]] = item
            new_data_dict=json.dumps(new_data_dict, indent=4)
            data = json.loads(new_data_dict)
            return data
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}
    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()
# Get the inventory.
ExampleInventory()
