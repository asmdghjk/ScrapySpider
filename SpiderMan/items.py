# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

class SpidermanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DianpingItemLoader(ItemLoader):
    pass
class DianpingItem(scrapy.Item):

        shopId = scrapy.Field()
        cityId = scrapy.Field()
        city = scrapy.Field()
        fullName = scrapy.Field()
        categoryId = scrapy.Field()
        categoryName = scrapy.Field()
        position = scrapy.Field()
        latitude = scrapy.Field()
        longitude = scrapy.Field()
        address = scrapy.Field()
        shopPower = scrapy.Field()
        avgPrice = scrapy.Field()
        phoneNo = scrapy.Field()
        isOversea = scrapy.Field()
        introduce = scrapy.Field()
        roomNums = scrapy.Field()
        hotelFloors = scrapy.Field()
        openningTime = scrapy.Field()
        decoDate = scrapy.Field()
        checkInTime = scrapy.Field()
        checkOutTime = scrapy.Field()
        scoreText = scrapy.Field()
        reviewAbstractText = scrapy.Field()
        reviewCount = scrapy.Field()
        imageURL = scrapy.Field()

        imagePath = scrapy.Field()

        def get_insert_sql(self):
                # 插入知乎question表的sql语句
                insert_sql = """
                insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num,
                  create_time, update_time, crawl_time
                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
                  update_time=VALUES(update_time)
            """

                create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
                update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
                params = (
                        self["zhihu_id"], self["url"], self["question_id"],
                        self["author_id"], self["content"], self["parise_num"],
                        self["comments_num"], create_time, update_time,
                        self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
                )

                return insert_sql, params
