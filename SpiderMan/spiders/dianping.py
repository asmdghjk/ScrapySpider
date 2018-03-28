# -*- coding: utf-8 -*-
import json,os

import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver

from items import DianpingItemLoader, DianpingItem


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['m.dianping.com']
    start_urls = ['https://m.dianping.com/']

    def __init__(self):
        # from pyvirtualdisplay import Display
        # display = Display(visible=0, size=(1024,768))
        # display.start()

        # 设置chromedriver不加载图片
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        driver_path = os.path.join(os.path.abspath('./SpiderMan/tools'), 'chromedriver.exe')
        print(driver_path)
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_opt)
        super(DianpingSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        #当爬虫退出的时候关闭chrome
        print ("spider closed")
        self.browser.quit()

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'SpiderMan.middlewares.JSPageMiddleware': 1
            # 'SpiderMan.middlewares.SpidermanSpiderMiddleware': 543,
        },

        'ITEM_PIPELINES' : {
            # 'SpiderMan.pipelines.ImagePipeline': 1,
            # 'SpiderMan.pipelines.TestPipeline': 100,
            'SpiderMan.pipelines.CsvWithEncodingPipeline': 2,
        },

        'MIN_WIDTH' : 100,
        'MIN_HEIGHT' : 100,
        'IMAGES_URLS_FIELD' : "imageURL",
        'IMAGES_STORE' : os.path.join(os.path.abspath(os.path.dirname('../../')),'images'),
        'DOWNLOAD_DELAY' : 2
    }


    headers = {
        "HOST": "m.dianping.com",
        "Referer": "https://m.dianping.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    start_list_url = "https://m.dianping.com/otahotel/hotelm/search?cityid=2&locatecityid=&mylng=&mylat=&lng=&lat=&hotelstarids=&pricerange=&sortid=&limitresult=20&limitpageno={0}&searchtype=0&groupable=&filterids=&versionName=&regionid=0&parentregionid=-10000&regiontype=0&shopid=&range=&locationid="
    hotel_info_url = "https://m.dianping.com/hotelm/ajax/hotelInfo?shopId={0}"
    detail_info_url = "https://m.dianping.com/otahotel/hotelm/detailInfo?shopid={0}"
    hotel_review_url = "https://m.dianping.com/hotelm/ajax/hotelReview?shopId={0}"

    def parse(self, response):
        return scrapy.Request(self.start_list_url.format(0), headers=self.headers,
                              meta={'pageno': 0},callback=self.parse_list)

    # 获取酒店列表
    def parse_list(self,response):
        if (response.status == 200):
            json_ = json.loads(response.text)
            if(json_['code'] == 200):
                for json_list in json_['data']['shopList']:
                    shopId = int( json_list['shopId'] )

                    # 酒店信息
                    yield scrapy.Request(self.hotel_info_url.format(shopId),
                                         meta={'shopId':shopId},headers=self.headers, callback=self.parse_info)

                pageno = response.meta["pageno"] + 1
                print("############# page number is : ",pageno)
                yield scrapy.Request(self.start_list_url.format(int(pageno)), headers=self.headers,
                                    meta={'pageno': pageno},callback=self.parse_list)

    # 酒店信息
    def parse_info(self,response):
        if (response.status == 200):
            json_ = json.loads(response.text)
            shopId = int(response.meta['shopId'])
            if(json_['code'] == 200):
                items = response.meta
                items["cityId"] = json_['data']['cityId']
                items["city"] = json_['data']['city']
                items["fullName"] = json_['data']['fullName']
                items["categoryId"] = json_['data']['categoryId']
                items["categoryName"] = json_['data']['categoryName']
                items["position"] = json_['data']['position']
                items["latitude"] = json_['data']['latitude']
                items["longitude"] = json_['data']['longitude']
                items["address"] = json_['data']['address']
                items["shopPower"] = json_['data']['shopPower']
                items["avgPrice"] = json_['data']['avgPrice']
                items["phoneNo"] = json_['data']['phoneNo']

                items["imageURL"] = json_['data']['picList'][0].get('url','')


                # 酒店详情信息
                yield scrapy.Request(self.detail_info_url.format(shopId),
                                     meta=items, headers=self.headers, callback=self.parse_detail)

    # 酒店详情信息
    def parse_detail(self, response):
        if (response.status == 200):
            json_ = json.loads(response.text)
            shopId = int(response.meta['shopId'])
            if (json_['code'] == 200):
                items = response.meta

                items["isOversea"] = json_['data']['shopInfos']['isOversea']
                items["introduce"] = json_['data']['shopInfos']['introduce']
                items["roomNums"] = json_['data']['shopInfos']['roomNums']
                items["hotelFloors"] = json_['data']['shopInfos']['hotelFloors']
                items["openningTime"] = json_['data']['shopInfos']['openningTime']
                items["decoDate"] = json_['data']['shopInfos']['decoDate']
                items["checkInTime"] = json_['data']['shopInfos']['checkInTime']
                items["checkOutTime"] = json_['data']['shopInfos']['checkOutTime']

                # 酒店评价
                yield scrapy.Request(self.hotel_review_url.format(shopId),
                                     meta=items, headers=self.headers, callback=self.parse_review)

    # 酒店评价
    def parse_review(self, response):
        if (response.status == 200):
            json_ = json.loads(response.text)
            if (json_['code'] == 200):
                items = response.meta

                items["scoreText"] = json_['data']['scoreText']
                items["reviewAbstractText"] = json_['data']['reviewAbstractText']
                items["reviewCount"] = json_['data']['reviewCount']

                item_loader = DianpingItemLoader(item=DianpingItem(), response=response)
                getAll = ['shopId', 'cityId', 'city', 'fullName', 'categoryId', 'categoryName', 'position', 'latitude',
                          'longitude', 'address', 'shopPower', 'avgPrice', 'phoneNo', 'shopId', 'isOversea',
                          'introduce', 'roomNums', 'hotelFloors', 'openningTime', 'decoDate', 'checkInTime',
                          'checkOutTime', 'shopId', 'scoreText', 'reviewAbstractText', 'reviewCount', 'imageURL']
                for key in items:
                    if key in getAll:
                        item_loader.add_value(key, items[key])
                yield item_loader.load_item()





