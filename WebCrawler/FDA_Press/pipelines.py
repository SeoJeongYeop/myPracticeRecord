# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import json

class FdaPressPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        json_file = "mysql_config.json"
        json_key = "root"
        with open(json_file) as f:
            data = json.load(f)
        user_values = data[json_key]

        self.connection = pymysql.connect(
            user=user_values["user"],
            passwd=user_values["password"],
            host=user_values["host"],
            db= user_values["database"],
            charset=user_values["charset"]
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
    def create_table(self) :
        tableName = 'crawlingNews712'
        self.cursor.execute(f""" DROP TABLE IF EXISTS {tableName}; """)
        self.cursor.execute(f""" CREATE TABLE {tableName}(id INT(11) NOT NULL AUTO_INCREMENT, title TEXT NOT NULL, created TEXT, contents TEXT NOT NULL, PRIMARY KEY (id)); """)
    def process_item(self, item, spider):
        self.store_in_db(item)
        return item
    def store_in_db(self, item) :
        tableName = 'crawlingNews712'
        command = f"""INSERT INTO {tableName} (title, created, contents) VALUES ("{item['title'][0]}","{item['date'][1]}","{item['contents'][0]}");"""
        self.cursor.execute(command)
        self.connection.commit()
