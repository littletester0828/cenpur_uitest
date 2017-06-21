#!/usr/bin/env python
#coding=utf-8
import os,sys
sys.path.append('..')
from pyse.init_pyse import Pyse
from time import sleep


open_sig_loc = ('xpath',".//*[@id='searchResult']/div[1]/dl[1]/dd[1]/table/tbody/tr/td[9]/p[2]/a")
frame_id='layui-layer-iframe1'
usb_dir = os.path.abspath('..') + "\\utils\\usbkey.exe"
add_sign_loc = ('id','addSign')
#sign_loc = ('xpath',".//*[@id='pageContainer5']/div[2]/div[35]")
#sign_loc = ('xpath',".//*[@id='pageContainer5']/div[2]/div[33]")
buyer_sign_loc = ('xpath',".//*[@id='pageContainer1']/div[2]/div[7]")
seller_sign_loc = ('xpath',"//*[@id='pageContainer1']/div[2]/div[6]")
confm_sign = ('xpath','//*[@id="finishSign"]/span')
close_sign = ('xpath','//*[@id="layui-layer1"]/span/a[3]')
mail_loc = ('xpath','//*[@id="pageContainer5"]/div[2]/div[44]')
#待签章




class BuyerSign(Pyse):
    def __init__(self,driver):
        self.driver = driver

    #打开签章页面
    def open_sig_page(self):
        self.click(open_sig_loc)
        sleep(5)

    #切换到签章frame
    def switch_to_frame(self):
        self.driver.switch_to.frame(frame_id)

    def switch_to_page(self):
        self.driver.switch_to.default_content()

    #点击签章按钮
    def opr_add_sign(self):
        self.click(add_sign_loc)

    #输入ukey密码
    def input_ukey_pwd(self):
        print(usb_dir)
        os.system(usb_dir)
        sleep(3)

    #买家找签章位置并签章
    def click_buyer_sign(self):
        self.click(buyer_sign_loc)
        sleep(3)

    #卖家找签章位置并签章
    def click_seller_sign(self):
        self.click(seller_sign_loc)
        sleep(3)

    #完成签章
    def confirm_sign(self):
        self.click(confm_sign)
        sleep(10)

    def close_sign(self):
        self.click(close_sign)
        sleep(1)


