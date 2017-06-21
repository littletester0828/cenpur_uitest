import time
import unittest
from pyse.init_pyse import Pyse
from utils.loadyaml import *
from testlibs.log import Logger
from utils.pymysql import selectBySql
import traceback

autolog = Logger()
userId="9c9689311f034619b8d22640154e6ffc"
shopMsg= selectBySql("select * from cenpur_mall_shop where mem_user_id='9c9689311f034619b8d22640154e6ffc'")
shopName=shopMsg[2]#公司名
shopPro = shopMsg[6]#公司介绍
majorGoods=shopMsg[12]#主营商品
majorType = shopMsg[13]#主营类型
mainHarhour=shopMsg[7]#主要港口
contacts = shopMsg[8]#联系人
contactsInformation=shopMsg[3]#联系方式
qqNumber = shopMsg[4]#qq号码


class TestStoreDeatil(unittest.TestCase):
    def setUp(self):
        self.driver = Pyse('chrome')
        self.driver.open(get_url("shopDetail_page"))
        #登录
        self.driver.login()
        time.sleep(2)
    '''
    项目开始setUp
    登录
    '''

    def test_1_storeImg(self):
        pass
        '''
        src = self.driver.get_attribute(get_element("storeDetail_page", "store_img_loc"),"src")
        if src:
          self.driver.open(str("http://10.82.12.25/centralize-purchase/"+src))
          assert self.driver.get_title()!="404 Not Found"
          # self.assertEqual(self.driver.get_title(), "404 Not Found", "店铺头像打开失败！")
          autolog.info("店铺页面图片展示正常")
        else:
          autolog.info("无法获取src")
          assert False,("获取src失败")       
        '''
    '''
    test_1_storeImg
    店铺图片(头像)展示
    获取图片src并访问
    '''
    def test_2_shopName(self):
        autolog.info("店铺名数据库显示："+shopName)
        text = self.driver.text_in_element(get_element("storeDetail_page", "shopName_text_loc"),shopName)
        autolog.info(text)
        assert text !=0
        # self.assertEqual(text,0,"店铺名与实际不符")
        autolog.info("店铺名正常")
    '''
    test_2_shopName
    店铺名显示，与数据库数据对比
    '''
    def test_3_majorGoods(self):
        '''主营商品展示'''
        autolog.info("主营商品数据库显示："+majorGoods)
        text = self.driver.text_in_element(get_element("storeDetail_page","majorGoods_text_loc"),majorGoods)
        autolog.info(text)
        assert text==1
        autolog.info("主营商品信息显示正常")
    '''
    test_3_majorGoods
    主营商品展示，与数据库做对比
    '''

    def test_4_majorType(self):
        '''主营品牌显示'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "majorType_text_loc"),majorType)
        autolog.info(text)
        assert text == 1
        autolog.info("主营品牌显示正常")
    '''
    test_4_majorType
    主营品牌显示，与数据库做对比
    '''

    def test_5_mainHarhour(self):
        '''常用港口展示'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "mainHarhour_text_loc"),mainHarhour)
        autolog.info(text)
        assert text == 1
        autolog.info("主营品牌显示正常")
    '''
    test_5_majorHarhour
    常用港口展示，与数据库做对比
    '''

    def test_6_contacts(self):
        '''联系人展示'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "contacts_text_loc"),contacts)
        autolog.info(text)
        assert text == 1
        autolog.info("联系人显示正常")
    '''
    test_6_contacts
    联系人展示，与数据库做对比
    '''

    def test_7_contactsInformation(self):
        '''联系方式'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "contactsInformation_text_loc"),contactsInformation)
        autolog.info(text)
        assert text == 1
        autolog.info("联系方式显示正常")
    '''
    test_7_contactsInformation
    联系方式展示，与数据库做对比
    '''
    def test_8_qqNumber(self):
        '''qq号码'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "qqNumber_text_loc"),qqNumber)
        autolog.info(text)
        assert text != 0
        autolog.info("qq号码显示正常")
    '''
    test_8_qqNumber
    QQ号码展示，与数据库做对比
    '''
    def test_9_1_shopPro(self):
        '''公司介绍信息'''
        text = self.driver.text_in_element(get_element("storeDetail_page", "shopPro_text_loc"), shopPro)
        autolog.info(text)
        assert text == 1
        autolog.info("公司介绍信息显示正常")

    '''
    test_9_shopPro
    公司信息展示，与数据库做对比
    '''
    def test_9_2_carAlert(self):
        '''加入购物车-弹窗-去看看按钮跳转购物车页面'''
        try:
            dic = self.driver.load_table("storeDetail_page","table_data_loc","table_name_loc")
            autolog.info(dic)
            self.driver.click(get_element("storeDetail_page","firstLineCar_button_loc"))
            time.sleep(1)
            words = self.driver.get_attribute(get_element("storeDetail_page","alertWords_text_loc"),"text")
            autolog.info(words)
            self.driver.click(get_element("storeDetail_page","alertGoToSee_button_loc"))
            time.sleep(1)
            now_url=self.driver.get_current_url()
            autolog.info(now_url)
            assert now_url=="http://10.82.12.25/centralize-purchase/#/shoppingCart",("未成功跳转页面")
            autolog.info("成功跳转购物车页")
        except:
            error = traceback.format_exc()
            autolog.error(error)
            assert False
    '''
    test_10_carAlert
    加入购物车弹窗
    验证是否能获取到表格信息
    点击第一行数据的加入购物车按钮
    通过弹窗进入购物车页面
    '''
    def test_9_3_collection(self):
        '''加入收藏按钮变色验证'''
        try:
            dic = self.driver.load_table("storeDetail_page","table_data_loc","table_name_loc")
            autolog.info(dic)
            loc =get_element("storeDetail_page","firstLineCollection_button_loc")
            #点击前
            class1 = self.driver.get_attribute(loc,"class")
            autolog.info("点击收藏前的class：%s"%class1)
            self.driver.click(loc)
            time.sleep(1)
            #点击后
            class2 = self.driver.get_attribute(loc,"class")
            autolog.info("点击收藏后的class%s"%class2)
            assert class2!=class1,("收藏后未变色")
            autolog.info("成功点击后变色")
        except:
            error = traceback.format_exc()
            autolog.error(error)
            assert False
    '''
    test_11_collection
    点击收藏按钮，验证点击后是否变色（点击前后button的class是否不同）
    '''
    def tearDown(self):
        self.driver.quit()
        autolog.info("tearDown")
if __name__ == "__main__":
    unittest.main()
