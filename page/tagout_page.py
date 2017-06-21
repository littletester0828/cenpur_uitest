# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from pyse.init_pyse import Pyse
from page.login_page import login_url, LoginPage
from page.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

order_num = None

class TagoutPage(Pyse):
    #交易方式（1）洽谈
    negotiation_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[1]')
    #交易方式（2）一口价
    fixed_price_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[2]')
    #交易方式（3）竞价
    auction_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[2]/dl/dd/div/a[3]')
    #品种
    type_loc = ('xpath', '/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/button')
    type_locs = ('xpath', '/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/ul/li[3]/a')
    #品名
    commodity_name_loc = ('id', 'brandAll')
    commodity_names_loc = ('xpath', '//*[@id="brandList"]/li[3]/a')
    #钢厂
    steel_factory_loc = ('id','factoryName')
    steel_factoryname_loc =('xpath','/html/body/div[7]/div[2]/div/div[5]/dl[5]/dd/div/ul/li[2]/a')
    #规格
    specName_loc =('id','specName')
    #材质
    materialName_loc = ('id','materialName')
    #负差
    difference_loc = ('id','difference')
    #计量方式(1)理计
    meterage_type_loc1 = ('xpath','/html/body/div[7]/div[2]/div/div[7]/dl/dd/div/a[1]')
    #计量方式(2)过磅
    meterage_type_loc2 = ('xpath','/html/body/div[7]/div[2]/div/div[7]/dl/dd/div/a[2]')
    #发盘量
    tagout_amount_loc = ('id','amount')
    #单价
    price_loc = ('id', 'price')
    #理计量
    call_amount_loc = ('id','callAmount')
    #起订量
    min_buy_loc = ('id','minBuy') 
    #时间控件
    time_loc = ('id','dueTime')
    #确认
    sure_button_loc = ('id','sureButton')

    def __init__(self, driver):
        self.driver = driver

    #选择交易模式
    def select_trading_model(self):
        self.find_element(self.fixed_price_loc).click()

    #选择品种
    def select_type(self):
        self.find_element(self.type_loc).click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/button')\
            .find_element_by_xpath('/html/body/div[7]/div[2]/div/div[5]/dl[1]/dd/div/ul/li[3]/a').click()

    #选择品名
    def select_commodity_name(self):
        self.find_element(self.commodity_name_loc).click()
        sleep(2)
        self.driver.find_element_by_id('brandAll')\
            .find_element_by_xpath('//*[@id="brandList"]/li[3]/a').click()

    #选择钢厂
    def select_factoryname(self):
        self.find_element(self.steel_factory_loc).click()
        sleep(2)
        self.driver.find_element_by_id('factoryName')\
            .find_element_by_xpath('/html/body/div[7]/div[2]/div/div[5]/dl[5]/dd/div/ul/li[2]/a').click()

    #输入规格
    def input_spc(self,spc='5*25'):
        self.send_keys(self.specName_loc,spc)

    #输入材质
    def input_materialName(self,materialName='合金钢'):
        self.send_keys(self.materialName_loc,materialName)

    #输入负差
    def input_difference(self,difference='5'):
        self.send_keys(self.difference_loc,difference)

    #选择计量方式
    def select_magerate_type(self):
        self.find_element(self.meterage_type_loc2).click()

    #输入发盘量
    def input_tagout_amount(self,tagoutmount='500'):
        self.send_keys(self.tagout_amount_loc,tagoutmount)

    #输入价格
    def input_price(self,price='50'):
        self.send_keys(self.price_loc,price)
    
    #输入理算量
    def input_callAmount(self,call_amount='0.5'):
        self.send_keys(self.call_amount_loc,call_amount)
        
    #输入起订量
    def input_min_buy(self,min_buy='10'):
        self.send_keys(self.min_buy_loc,min_buy)

    #输入截止日期
    def input_time(self,value='2017-12-30'):
        js = 'document.getElementById(\'dueTime\').removeAttribute(\'readonly\');'
        self.driver.execute_script(js)
        self.send_keys(self.time_loc, value)

    #移动到浏览器底部
    def scroll_to_low(self):
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)  

    #点击确定按钮
    def click_sure(self):
        self.click(self.sure_button_loc)

    #商品挂牌流程
    def tagout(self,dr):
        self.select_trading_model()
        self.select_type()
        sleep(2)
        self.select_commodity_name()
        sleep(2)
        self.select_factoryname()
        self.input_spc()
        self.input_materialName()
        self.input_difference()
        self.input_tagout_amount()
        self.input_price()
        self.input_callAmount()
        self.input_min_buy()
        self.input_time()
        self.scroll_to_low()
        self.click_sure()
        WebDriverWait(dr, 5, 1).until(EC.title_contains("我的商品 - 中联钢信"))
        commodity_num = self.find_element(('xpath', '//*[@id="searchResult"]/div[1]/dl[1]/dt/label[1]/input')).get_attribute("value")
        return commodity_num


if __name__ == '__main__':
    login = LoginPage("firefox")
    login.open(login_url)
    login.login('18215526975', 'ZFf12345')

    d = login.get_driver()
    print(type(d))
    # driver = login.login_pg_rt_driver()
    WebDriverWait(d, 5, 1).until(EC.title_contains("首页 - 中联钢信"))
    # sleep(5)
    print(d.title)
    user_name = d.find_element_by_css_selector(".fr>li>h6>a").text
    print("user_name:", user_name)
    page = HomePage(d)
    page.click_tagout()
    tagpage = TagoutPage(d)
    tests = tagpage.tagout()
    print(tests)
    print("done")


