# -*- coding:utf-8 -*-

import time
import unittest
from pyse.init_pyse import Pyse
from utils.loadyaml import *
from testlibs.log import Logger
from utils.pymysql import *
import traceback

autolog = Logger()
getPerson_value = "阎海源"
deatilAdress_value = "详细地址天府三街"
companyName_value = "大数金科网络技术有限公司"
contactInformation_value = "15737957635"
horbor_value="安多利威亚港口"
user_id="9c9689311f034619b8d22640154e6ffc"


class TestAdress(unittest.TestCase):
    def setUp(self):
        self.url="addressManger_page"
        self.driver = Pyse('chrome')
        self.driver.open(get_url("home_page"))
        #登录
        self.driver.login()
        self.driver.click(get_element("home_page", "member_href_loc"))
        self.driver.click(get_element("member_page", "addressManager_href_loc"))
    '''
    setUp
    进入首页登录
    再进入地址管理页面
    '''
    def test_1_newGetAdress(self):
        '''新建收货地址'''
        # 清空数据库地址信息
        selectBySql("delete from cenpur_user_address where user_id ='%s'"%user_id)
        aaa = selectBySql("select * from cenpur_user_address where user_id ='%s'" % user_id)
        autolog.info(aaa)

        time.sleep(2)
        #输入地址信息
        self.driver.click(get_element("addressManger_page","newGetAdress_button_loc"))
        autolog.info("点击新增收货地址")
        self.driver.send_keys(get_element("addressManger_page", "getPerson_textBox_loc"),getPerson_value)
        autolog.info("填写收货人")
        self.driver.send_keys(get_element("addressManger_page","deatilAdress_textBox_loc"),deatilAdress_value)
        autolog.info("填写详细地址")
        self.driver.send_keys(get_element("addressManger_page","companyName_textBox_loc"),companyName_value)
        autolog.info("填写公司名称")
        self.driver.send_keys(get_element("addressManger_page","contactInformation_textBox_loc"),contactInformation_value)
        autolog.info("填写联系方式")
        self.driver.click(get_element("addressManger_page","keep_button_loc"))
        autolog.info("点击保存")
        try:
            data =self.driver.load_table("addressManger_page","data_table_loc","name_table_loc")
            if data:
                autolog.info(data)
                assert True
            else:
                autolog.info(data)
                assert False,("数据错误")
        except:
            autolog.error(traceback.format_exc())
            assert False,("未获取到表格数据")
    '''
    test_1_newGetAdress
    新建收货地址
    数据库清空我的地址
    新建地址后查询页面是否显示
    '''

    def test_2_newPostAdress(self):
        '''新增发货地址'''
        # 清空数据库地址信息
        selectBySql("delete from cenpur_user_address where user_id =%s" % user_id)
        time.sleep(2)
        self.driver.click(get_element("addressManger_page","postAdress_span_loc"))
        time.sleep(1)
        self.driver.click(get_element("addressManger_page", "newGetAdress_button_loc"))
        autolog.info("点击新增收货地址")
        self.driver.send_keys(get_element("addressManger_page", "getPerson_textBox_loc"), getPerson_value)
        autolog.info("填写收货人")
        self.driver.send_keys(get_element("addressManger_page", "deatilAdress_textBox_loc"), deatilAdress_value)
        autolog.info("填写详细地址")
        self.driver.send_keys(get_element("addressManger_page", "companyName_textBox_loc"), companyName_value)
        autolog.info("填写公司名称")
        self.driver.send_keys(get_element("addressManger_page", "postContactInformation_text_loc"), contactInformation_value)
        autolog.info("填写联系方式")
        self.driver.send_keys(get_element("addressManger_page","horbor_textBox_loc"),horbor_value)
        autolog.info("填写仓库、港口信息")
        self.driver.click(get_element("addressManger_page", "post_button_loc"))
        autolog.info("点击保存")
        try:
            data = self.driver.load_table("addressManger_page", "data_table_loc", "name_table_loc")
            if data:
                autolog.info(data)
                assert True
            else:
                autolog.info(data)
                assert False, ("数据错误")
        except:
            autolog.error(traceback.format_exc())
            assert False, ("未获取到表格数据")
    '''
    test_2_newPostAdress
    新建发货地址
    数据库清空我的地址
    新建地址后查询页面是否显示
    '''

    def tearDown(self):
        self.driver.close()
        autolog.info("tearDown")

if __name__ == "__main__":
    unittest.main()
