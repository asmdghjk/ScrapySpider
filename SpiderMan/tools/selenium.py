#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time

from selenium import webdriver
from scrapy.selector import Selector

class MySelenium:
    @classmethod
    def getBrowser(self, *args, **kwargs):
        browser = webdriver.Chrome(executable_path=os.path.join(os.path.abspath('.'), 'chromedriver.exe'))
        return browser


# browser.get('https://www.zhihu.com/signup')
#
# browser.find_element_by_css_selector(".SignContainer-inner div.SignContainer-switch span").click()
# time.sleep(2)
# browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys("15630183192")
# browser.find_element_by_css_selector(".SignFlow-password div div.Input-wrapper input[name='password']").send_keys("ilovechina")
#
# browser.find_element_by_css_selector(".SignContainer-inner div.Login-content form button[type='submit']").click()

# t_selector = Selector(text=browser.page_source)


# browser.quit()