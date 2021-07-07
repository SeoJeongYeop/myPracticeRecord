# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class FdaPressPipeline:
    # def __init__(self):
    #     self.create_connection()
    #     self.create_table()

    # def create_connection(self):
    #     self.connection = pymysql.connect(
    #         user='root',
    #         passwd='{password}',
    #         host='127.0.0.1',
    #         db= 'FDA',
    #         charset='utf8'
    #     )
    #     self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
    # def create_table(self) :
    #     tableName = 'crawlingNews'
    #     self.cursor.execute(f""" DROP TABLE IF EXISTS {tableName}; """)
    #     self.cursor.execute(f""" CREATE TABLE {tableName}(id INT(11) NOT NULL AUTO_INCREMENT, title TEXT NOT NULL, created TEXT, contents TEXT NOT NULL, PRIMARY KEY (id)); """)
    def process_item(self, item, spider):
        # self.store_in_db(item)
        return item
    # def store_in_db(self, item) :
    #     tableName = 'crawlingNews'
    #     command = f"""INSERT INTO {tableName} (title, created, contents) VALUES ("{item['title']}","{item['date']}","{item['contents']}");"""
    #     self.cursor.execute(command)
    #     self.connection.commit()
