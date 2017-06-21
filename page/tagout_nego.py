# -*- coding:utf-8 -*-
import os,sys
sys.path.append('../')

from time import sleep
from pyse.init_pyse import Pyse
from page.login_page import login_url, LoginPage
from page.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TagoutPage(Pyse):
    negotiation_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[1]')
    fixed_price_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[2]')
    auction_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[3]')
    type_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/button')
    type_locs = ('xpath', '/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/ul/li[3]/a')


    def __init__(self, driver):
        self.driver = driver

    def select_trading_model(self):
        self.find_element(self.fixed_price_loc).click()

    def select_type(self):
        sleep(2)
        self.find_element(self.type_loc).click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/button')\
            .find_element_by_xpath('/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/ul/li[3]/a').click()
        #self.find_element(self.type_locs).click()


if __name__ == '__main__':
    login = LoginPage()
    login.open(login_url)
    login.login('13331133831', 'Aa1234')

    d = login.get_driver()
    print(type(d))
    # driver = login.login_pg_rt_driver()
    WebDriverWait(d, 5, 1).until(EC.title_contains("首页 - 中联钢信"))
    # sleep(5)
    print(d.title)
    user_name = d.find_element_by_css_selector(".fr>li>h6>a").text
    print("user_name:", user_name)
    page = HomePage(d)
    page.guapai()
    tagpage = TagoutPage(d)
    print(tagpage.get_driver())
    tagpage.select_trading_model()
    print('######################')
    tagpage.select_type()
    print("done")


