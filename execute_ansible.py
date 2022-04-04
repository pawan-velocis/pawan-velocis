import ansible_runner
import json
from pymongo import MongoClient
import sys
def delete_data_from_db():
    try:
        myclient = MongoClient("mongodb://10.18.1.53:27017/")
        db = myclient["psirt"]
        try:
            Collection = db["Non_DNAC_ANSIBLE"]
        except pymongo.errors.CursorNotFound:
            print("Cursor Not Found")
    except:
        print("Could not connect to MongoDB")
    try:
        result= Collection.delete_many({})
    except pymongo.errors.PyMongoError:
        print("Collection delete error")

def ansible_playbook_runner(query):
    insertAllVulenrablityHostWise(query)
    try:
        out, err, rc = ansible_runner.run_command(
        executable_cmd='ansible-playbook',
        cmdline_args=['cisco_show_ver_ios.yml', '-i', 'customdynamicinventory.py','-vvvv'],
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,
        )
    except:
        print("Could not run ansible")
    print("rc: {}".format(rc))
    print("out: {}".format(out))
    print("err: {}".format(err))
    delete_data_from_db()
    return out

def insertAllVulenrablityHostWise(resp_dict):
    print("insertAllVulenrablityHostWise: ", resp_dict)
    try:
        myclient = MongoClient("mongodb://10.18.1.53:27017/")
        db = myclient["psirt"]
        try:
            Collection = db["Non_DNAC_ANSIBLE"]
        except pymongo.errors.CursorNotFound:
            print("Cursor Not Found")
    except pymongo.errors.ConnectionFailure:
        print("Could not connect to MongoDB")
    if isinstance(resp_dict, list):
        try:
            print('many*************')
            Collection.insert_many(resp_dict, ordered=False, bypass_document_validation=True)
        except pymongo.errors.BulkWriteError as e:
            print(e.details['writeErrors'])
    else:
        try:
            print('One*************')
            Collection.insert_one(resp_dict)
        except pymongo.errors.WriteError:
            print("Insertion Error")

json_str=[
            {
                'Groups': 'Group1',
                'hosts': '10.122.1.2',
                'ansible_ssh_user': 'raj1',
                'ansible_ssh_pass': 'Pass2006',
                'ansible_network_os': 'ios',
                'ansible_python_interpreter': '/usr/bin/python3',
                '_meta':'_meta',
                'vars':'ansible_ssh_user,ansible_ssh_pass,ansible_network_os,ansible_python_interpreter'
            },
            {
                'Groups': 'Group2',
                'hosts': '10.126.1.2',
                'ansible_ssh_user': 'raj1',
                'ansible_ssh_pass': 'Pass2006',
                'ansible_network_os': 'ios',
                'ansible_python_interpreter': '/usr/bin/python3',
                '_meta':'_meta',
                'vars':'ansible_ssh_user,ansible_ssh_pass,ansible_network_os,ansible_python_interpreter'
            }
         ]
query = json.dumps(json_str, sort_keys=True)
ansible_playbook_runner(json_str)
