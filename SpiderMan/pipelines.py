# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import codecs,json
import pymysql


class SpidermanPipeline(object):
    def process_item(self, item, spider):
        return item


# 自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('hotel.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 自定义csv文件的导出
class CsvWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('hotel.csv', 'w', encoding="utf-8")
        self.file.write('shopId,cityId,city,fullName,categoryId,categoryName,position,latitude,longitude,address,shopPower,avgPrice,phoneNo,shopId,isOversea,introduce,roomNums,hotelFloors,openningTime,decoDate,checkInTime,checkOutTime,shopId,scoreText,reviewAbstractText,reviewCount,imageURL')

    def process_item(self, item, spider):
        lines = 'shopId', item['cityId', item['city', item['fullName', item['categoryId', item['categoryName', item['position', item['latitude',
                          item['longitude', item['address', item['shopPower', item['avgPrice', item['phoneNo', item['shopId', item['isOversea',
                          item['introduce', item['roomNums', item['hotelFloors', item['openningTime', item['decoDate', item['checkInTime',
                          item['checkOutTime', item['shopId', item['scoreText', item['reviewAbstractText', item['reviewCount', item['imageURL' + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 异步线程保存到Mysql
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 自定义图片的导出
class ImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "imageURL" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["imagePath"] = image_file_path
        return item


