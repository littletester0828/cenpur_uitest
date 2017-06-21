#!/usr/bin/env python
#coding=utf-8

import os, sys
sys.path.append('../')
from time import sleep
from pyse.init_pyse import Pyse

go_buy = ('xpath','html/body/div[8]/div[1]/div[3]/div[5]/button[1]')
sub_order = ('xpath','html/body/div[10]/div[4]/div[2]/div[2]/div/input')
confm_adress = ('xpath',".//*[@id='layui-layer1']/div[3]/a[1]")



#sys.exit("sorry, goodbye!")

class BuyCommodity(Pyse):

    def __init__(self,driver):
        self.driver = driver
    #获取商品定位
    def get_goods_loc(self,goods_id):
        self.refresh()
        sleep(2)
        print('goods_id:::', goods_id)
        goods_herf = "/zlgxjy/goods/detail.html?id=" + goods_id
        self.goods_loc = ('xpath', "//tbody/tr/td/a[@href='" + goods_herf + "']")
        return self.goods_loc
    #进入商品详情
    def find_goods(self,goods_id):
        self.find_element(self.get_goods_loc(goods_id)).click()
        sleep(2)

    #买家在商品详情进行购买下单
    def buyer_sub_order(self):
        self.find_element(go_buy).click()
        self.click(sub_order)
        sleep(2)
        self.click(confm_adress)
        sleep(5)
        print(self.driver.title)


















