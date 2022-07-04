from pymongo import MongoClient
import ssl
import ast
connection = MongoClient('mongodb+srv://data:9ry4n5hu@cluster0.goomm.mongodb.net/data?retryWrites=true&w=majority')
def get_data():
        dbs = connection.data
        data = dbs.data
        list_of_data = data.find()
        string = ""
        for item in list_of_data:
                string = string + item['data']
        try:
                string = ast.literal_eval(string)
        except:
                string = {}
        return string

def update(datas):
        datas = str(datas)
        dbs = connection.data
        data = dbs.data
        list_of_data = data.find()
        string = ""
        for item in list_of_data:
                mydb = connection['data']
                mycol = mydb['data']
                mycol.update_one(item, {'$set':{'data' : datas}})
        return True

