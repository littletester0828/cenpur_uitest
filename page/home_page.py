# -*- coding=utf-8 -*-

import sys
sys.path.append('../')

from selenium import webdriver
from page.login_page import login_url, LoginPage
from pyse.init_pyse import Pyse
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class HomePage(Pyse):
    #我是卖家
    seller_loc = ('xpath', 'html/body/div[1]/div/ul/li[9]/h6/b')
    #我是买家
    buyer_loc = ('xpath', 'html/body/div[1]/div/ul/li[11]/h6/b')
    #商品挂牌
    commodity_tagout_loc = ('xpath', 'html/body/div[1]/div/ul/li[9]/h6/div/a[1]')
    #我的销售订单
    my_sales_order_loc = ('xpath', 'html/body/div[1]/div/ul/li[9]/h6/div/a[3]')
    #销售订单
    sales_order_loc = ('xpath', '/html/body/div[7]/div[1]/dl[1]/dd/ul[3]/li/a')
    #待签章
    wait_sig_loc = ('xpath', "/html/body/div[7]/div[2]/div/div[1]/ul/li[2]/a")
    #现货市场
    market_loc = ('xpath', ".//*[@id='navigation_1']")

    def __init__(self, driver):
        self.driver = driver

    #点击“卖家”
    def click_seller(self):
        self.move_to_element(self.seller_loc)

    #点击“商品挂牌”
    def click_tagout(self):
        self.click_seller()
        sleep(1)
        self.click(self.commodity_tagout_loc)

    #点击“我的销售订单”
    def my_sales_order(self):
        self.click_seller()
        # sleep()
        self.click(self.my_sales_order_loc)

    #点击“销售订单”
    def click_sales_order(self):
        self.click(self.sales_order_loc)

    #点击“待签章”
    def click_wait_sign(self):
        self.click(self.wait_sig_loc)
        self.refresh()
        sleep(2)

    #点击“现货市场”
    def click_market(self):
         self.click(self.market_loc)



if __name__ == '__main__':
    login = LoginPage('firefox')
    login.open(login_url)
    login.login('18215526975','ZFf12345')
    dr = login.get_driver()
    homepage = HomePage(dr)
    homepage.my_sales_order()
    dr = login.get_driver()
    WebDriverWait(dr, 5, 1).until(EC.title_contains("首页 - 中联钢信"))
    print(dr.title)
    




