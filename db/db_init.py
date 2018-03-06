import sqlite3, os, sys

db_path = os.path.dirname(sys.modules['__main__'].__file__) + "\database.db"

# SQL QUERIES THAT ARE RUN ON DB INIT

drop_items_table = "DROP TABLE IF EXISTS `items`"

drop_warehouses_table = "DROP TABLE IF EXISTS `warehouses`"

drop_classifications_table = "DROP TABLE IF EXISTS `classifications`"

create_classifications_table = """
CREATE TABLE IF NOT EXISTS `classifications` ( 
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,  
    `classification` TEXT 
);"""

create_warehouses_table = """
CREATE TABLE IF NOT EXISTS `warehouses` ( 
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,  
    `city` TEXT, 
    `latitude` REAL, 
    `longitude` REAL
);"""

create_items_table = """
CREATE TABLE IF NOT EXISTS `items` ( 
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,  
    `warehouse_id` INTEGER,
    `classification_id` INTEGER,
    `timestamp` INTEGER,
    `image_path` TEXT,
    FOREIGN KEY(`warehouse_id`) REFERENCES `warehouses`(`id`),
    FOREIGN KEY(`classification_id`) REFERENCES `classification`(`id`)
);"""

insert_vancouver_warehouse = """
INSERT INTO `warehouses` (city, latitude, longitude)
    VALUES ('Vancouver', 49.2616203, -123.2499701);"""

insert_red_class = "INSERT INTO `classifications` (classification) VALUES ('red');"""

insert_green_class = "INSERT INTO `classifications` (classification) VALUES ('green');"""

insert_blue_class = "INSERT INTO `classifications` (classification) VALUES ('blue');"""

insert_dummy_items = """
INSERT INTO `items` (warehouse_id, classification_id, timestamp, image_path) 
    VALUES  (1, 1, 123, '\\img\\1.jpg'),
            (1, 2, 124, '\\img\\2.jpg'),
            (1, 3, 125, '\\img\\3.jpg'),
            (1, 1, 126, '\\img\\4.jpg');"""

queries = [drop_items_table, drop_warehouses_table, drop_classifications_table,
            create_classifications_table, create_warehouses_table, create_items_table,
            # comment the line below to remove test data
            insert_vancouver_warehouse, insert_red_class, insert_green_class, insert_blue_class, insert_dummy_items]

print(db_path)

def db_init():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        for q in queries:
            print("Executing Query: " + q)
            print("")
            cursor.execute(q)

    print("Database initialized!")

if __name__ == "__main__":
    db_init()

# def create_connection(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         conn.close()
 
# if __name__ == "__main__":
#     create_connection(os.path.dirname(os.path.abspath(__file__)) + "\db\database.db")