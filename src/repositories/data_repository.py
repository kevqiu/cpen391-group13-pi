# from server import Item

import os, sys, sqlite3

class DataRepository:
    def __init__(self, db_path):
        self.db_path = os.path.dirname(sys.modules['__main__'].__file__) + db_path

    def get_items(self):
        try:
           with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM items')
                for row in cursor:
                    print(row, file=sys.stderr)
                #return cursor[0]
                return "here"
        except:
            print("err")
        return "shouldnt be here"
        # connection = sqlite3.connect(self.db_path)
        # return self.db_path
        # create_connection(db_path)

    def get_item(self, query, value):
        return ""

    # def get_item_test(self):
    #     test = Item.query.all()
    #     for i in test:
    #         print(i, file=sys.stderr)