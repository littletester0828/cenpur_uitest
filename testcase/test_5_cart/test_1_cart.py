# -*-coding:utf-8-*-
import time
import unittest
from pyse.init_pyse import Pyse
from testlibs.log import Logger
from utils.loadyaml import *
from utils.connectSQL import *
import re

autolog = Logger()


class TestMyCart(unittest.TestCase):

    def setUp(self):
        self.driver = Pyse('firefox')
        self.driver.open(get_url("home_page"))
        self.driver.click(get_element("login_page", "switch_button_loc"))
        current_handle = self.driver.switch_window()
        self.driver.send_keys(get_element("login_page", "username_input_loc"), "15881122294")
        self.driver.send_keys(get_element("login_page", "password_input_loc"), "Xian1016")
        self.driver.send_keys(get_element("login_page", "verifyCode_input_loc"), "8888")
        self.driver.click(get_element("login_page", "login_button_loc"))
        time.sleep(2)
        result_handle = self.driver.all_window_handles()
        self.assertNotIn(current_handle, result_handle, "登录失败，登录窗口未关闭！")
        self.driver.switch_to_single_window()
        self.driver.click(get_element("home_page", "product_href_loc"))
        time.sleep(2)
    '''
    case：加入购物车-入口验证-商品详情页面
    expected：
    成功将商品加入购物车
    '''
    def test_1_addCart_1_entry_1_goodsDetail(self):
        # 获取加入购物车商品名称
        all_goods_list = self.driver.load_table(
            "cart_page", "goodsList_table_data_loc", "goodsList_table_name_loc")
        all_goods_name_list = all_goods_list["商品名称"]
        # 跳转商品详情页面
        self.driver.find_element(get_element("cart_page", "goodsList_goodsName_text_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("cart_page", "goodsDetail_addCart_button_loc")), "跳转商品详情页面失败")
        # 获取购物车商品显示计数
        if self.driver.is_element_exist(get_element("cart_page", "goodsDetail_cartAccount_span_loc")):
            cart_goods_account_before = self.driver.find_element(
                get_element("cart_page", "goodsDetail_cartAccount_span_loc")).text
        else:
            cart_goods_account_before = 0
        # 加入购物车
        self.driver.find_element(get_element("cart_page", "goodsDetail_addCart_button_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("cart_page", "addCart_info_skipToCart_button_loc")), "加入购物车确认弹窗未弹出")
        # 继续购物
        self.driver.find_element(get_element("cart_page", "addCart_info_keepShopping_button_loc")).click()
        self.assertFalse(self.driver.is_element_exist(
            get_element("cart_page", "addCart_info_skipToCart_button_loc")), "加入购物车确认弹窗未关闭")
        if self.driver.is_element_exist(get_element("cart_page", "goodsDetail_cartAccount_span_loc")):
            cart_goods_account_after = self.driver.find_element(
                get_element("cart_page", "goodsDetail_cartAccount_span_loc")).text
        else:
            cart_goods_account_after = 0
        self.assertEqual(cart_goods_account_before+1, int(cart_goods_account_after), "购物车商品显示计数错误")
        # 再次加入购物车
        self.driver.find_element(get_element("cart_page", "goodsDetail_addCart_button_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("cart_page", "addCart_info_skipToCart_button_loc")), "加入购物车确认弹窗未弹出")
        # 去看看，跳转购物车页面
        current_url = self.driver.get_current_url()
        self.driver.find_element(get_element("cart_page", "addCart_info_skipToCart_button_loc")).click()
        cart_goods_account_again = self.driver.find_element(
            get_element("cart_page", "goodsCart_cartAccount_span_loc")).text
        self.assertEqual(int(cart_goods_account_after), int(cart_goods_account_again), "添加相同商品到购物车，显示计数错误")
        skip_url = self.driver.get_current_url()
        self.assertNotEqual(current_url, skip_url, "跳转购物车页面失败")
        # 获取购物车商品名称
        cart_goods_name = self.driver.find_element(get_element("cart_page", "cartGoods_name_text_loc")).text
        self.assertIn(all_goods_name_list[0], cart_goods_name, "商品详情页面-商品添加购物车失败")
        delete_sql = "DELETE FROM cenpur_mall_cart_goods where " \
                     "cart_id = (select id from cenpur_mall_cart where user_id = '26878e6d32df4e1c95b579af43990da4')"
        connect_sql(delete_sql)
    '''
    case：加入购物车-入口验证-店铺详情页面
    expected：
    成功将商品加入购物车
    '''
    def test_1_addCart_1_entry_2_shopDetail(self):
        self.driver.find_element(get_element("cart_page", "goodsList_goodsName_text_loc")).click()
        time.sleep(1)
        self.driver.find_element(get_element("cart_page", "enterShop_button_loc")).click()
        time.sleep(2)
        shop_goods_list = self.driver.load_table(
            "cart_page", "shopDetail_goodsList_table_data_loc", "shopDetail_goodsList_table_name_loc")
        shop_goods_name_list = shop_goods_list["商品品名"]
        if self.driver.is_element_exist(get_element("cart_page", "goodsCart_cartAccount_span_loc")):
            cart_goods_account_before = self.driver.find_element(
                get_element("cart_page", "goodsCart_cartAccount_span_loc")).text
        else:
            cart_goods_account_before = 0
        # 加入购物车
        self.driver.find_element(get_element("cart_page", "shopDetail_addCart_button_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("cart_page", "addCart_info_skipToCart_button_loc")), "加入购物车确认弹窗未弹出")
        # 继续购物
        self.driver.find_element(get_element("cart_page", "addCart_info_keepShopping_button_loc")).click()
        self.assertFalse(self.driver.is_element_exist(
            get_element("cart_page", "addCart_info_skipToCart_button_loc")), "加入购物车确认弹窗未关闭")
        if self.driver.is_element_exist(get_element("cart_page", "goodsCart_cartAccount_span_loc")):
            cart_goods_account_after = self.driver.find_element(
                get_element("cart_page", "goodsCart_cartAccount_span_loc")).text
        else:
            cart_goods_account_after = 0
        self.assertEqual(cart_goods_account_before + 1, int(cart_goods_account_after), "购物车商品显示计数错误")
        self.driver.find_element(get_element("cart_page", "shopDetail_addCart_button_loc")).click()
        self.driver.find_element(get_element("cart_page", "addCart_info_skipToCart_button_loc")).click()
        cart_goods_name = self.driver.find_element(get_element("cart_page", "cartGoods_name_text_loc")).text
        self.assertIn(shop_goods_name_list[0], cart_goods_name, "商品详情页面-商品添加购物车失败")
        delete_sql = "DELETE FROM cenpur_mall_cart_goods where " \
                     "cart_id = (select id from cenpur_mall_cart where user_id = '26878e6d32df4e1c95b579af43990da4')"
        connect_sql(delete_sql)
    '''
    case：加入购物车-商品采购量
    expected：
    修改默认商品采购量，购物车商品采购量正确显示
    '''
    def test_1_addCart_2_purchaseNum(self):
        self.driver.find_element(get_element("cart_page", "goodsList_goodsName_text_loc")).click()
        time.sleep(2)
        mini_order = self.driver.find_element(
            get_element("cart_page", "purchaseAccount_input_loc")).get_attribute("value")
        self.driver.find_element(get_element("cart_page", "purchaseAccount_input_loc")).clear()
        custom_order = int(mini_order) + 10
        self.driver.find_element(get_element("cart_page", "purchaseAccount_input_loc")).send_keys(custom_order)
        self.driver.find_element(get_element("cart_page", "goodsDetail_addCart_button_loc")).click()
        self.driver.find_element(get_element("cart_page", "addCart_info_skipToCart_button_loc")).click()
        goods_cart_purchase_account = self.driver.find_element(
            get_element("cart_page", "goodsCart_purchaseAccount_input_loc")).get_attribute("value")
        self.assertEqual(custom_order, int(goods_cart_purchase_account), "自定义商品采购量错误")
    '''
    case：加入购物车-购物车总价计算
    expected：
    总价 = 单价*采购量
    '''
    def test_2_cart_1_total(self):
        self.driver.find_element(get_element("cart_page", "myCart_button_loc")).click()
        goods_cart_purchase_account = self.driver.find_element(
            get_element("cart_page", "goodsCart_purchaseAccount_input_loc")).get_attribute("value")
        unit_price = re.sub("\D", "", self.driver.find_element(
            get_element("cart_page", "goodsCart_unitPrice_text_loc")).text)
        total = re.sub("\D", "", self.driver.find_element(get_element("cart_page", "goodsCart_total_text_loc")).text)
        self.assertEqual(int(total), int(goods_cart_purchase_account)*int(unit_price), "购物车商品总价错误")
    '''
    case：加入购物车-删除购物车商品
    expected：
    商品从购物车中移除
    '''
    def test_2_cart_2_deleteGoods(self):
        self.driver.find_element(get_element("cart_page", "myCart_button_loc")).click()
        time.sleep(2)
        self.assertTrue(self.driver.is_element_exist
                        (get_element("cart_page", "deleteGoods_button_loc")), "跳转购物车页面失败")
        self.driver.find_element(get_element("cart_page", "deleteGoods_button_loc")).click()
        time.sleep(2)
        self.assertFalse(self.driver.is_element_exist(
            get_element("cart_page", "cartGoods_name_text_loc")), "商品删除失败")
        self.driver.find_element(get_element("home_page", "shopDetail_member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        time.sleep(2)
        self.assertTrue(get_element("myFavorite_page", "myFavorite_goodsName_text_loc"), "购物车商品移入收藏夹失败")
        delete_sql = "DELETE FROM cenpur_mall_favorites where user_id = '26878e6d32df4e1c95b579af43990da4'"
        connect_sql(delete_sql)
    '''
    case：购物车-购物车商品加入收藏夹
    expected：
    购物车商品成功加入收藏夹
    '''
    def test_3_toFavorite_1_addToFavorite(self):
        self.driver.find_element(get_element("cart_page", "goodsList_goodsName_text_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("cart_page", "goodsDetail_addCart_button_loc")).click()
        self.driver.find_element(get_element("cart_page", "addCart_info_skipToCart_button_loc")).click()
        time.sleep(2)
        goods_name = self.driver.find_element(get_element("cart_page", "cartGoods_name_text_loc")).text
        self.driver.find_element(get_element("cart_page", "cart_addFavourite_button_loc")).click()
        self.driver.find_element(get_element("cart_page", "cart_member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        favorite_goods_name = self.driver.find_element(
            get_element("myFavorite_page", "myFavorite_goodsName_text_loc")).text
        self.assertEqual(goods_name, favorite_goods_name, "购物车商品加入收藏夹失败")
        delete_sql = "DELETE FROM cenpur_mall_favorites where user_id = '26878e6d32df4e1c95b579af43990da4'"
        connect_sql(delete_sql)
    '''
    case：购物车-购物车商品移入收藏夹
    expected：
    购物车商品成功加入收藏夹
    '''
    def test_3_toFavorite_2_shiftInFavorite(self):
        self.driver.find_element(get_element("cart_page", "myCart_button_loc")).click()
        time.sleep(2)
        goods_name = self.driver.find_element(get_element("cart_page", "cartGoods_name_text_loc")).text
        self.driver.find_element(get_element("cart_page", "cart_shiftInFavourite_button_loc")).click()
        time.sleep(1)
        self.assertFalse(self.driver.is_element_exist(
            get_element("cart_page", "cart_shiftInFavourite_button_loc")), "移入收藏夹，购物车列表删除失败")
        self.driver.find_element(get_element("cart_page", "cart_member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        time.sleep(2)
        favorite_goods_name = self.driver.find_element(
            get_element("myFavorite_page", "myFavorite_goodsName_text_loc")).text
        self.assertEqual(goods_name, favorite_goods_name, "购物车商品移入收藏夹失败")
        delete_sql = "DELETE FROM cenpur_mall_favorites where user_id = '26878e6d32df4e1c95b579af43990da4'"
        connect_sql(delete_sql)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
