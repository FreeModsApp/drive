from pymongo import MongoClient
import ssl
import ast
connection = MongoClient('mongodb+srv://data:9ry4n5hu@cluster0.tlda6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
def get_data() -> dict:
        dbs = connection.data
        data = dbs.data
        list_of_data = data.find()
        string = ""
        for item in list_of_data:
                string = string + item['data']
        string = ast.literal_eval(string)
        return string

def update(datas) -> bool:
        try:
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
        except:
                return False


# data store format 
# {'id' : 'key'}
# id = telegram id
# key = encryption key
