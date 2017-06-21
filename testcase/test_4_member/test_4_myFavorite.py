# -*-coding:utf-8-*-
import time
import unittest
from pyse.init_pyse import Pyse
from testlibs.log import Logger
from utils.loadyaml import *
from utils.connectSQL import *

autolog = Logger()


class TestMyFavourite(unittest.TestCase):

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
        self.driver.find_element(get_element("home_page", "product_href_loc")).click()
        time.sleep(2)

    '''
    case：加入收藏夹-商品收藏-商品详情页面
    expected：
    成功收藏商品
    '''
    def test_1_addFavorite_1_addGoods_1_goodsDetail(self):
        goods_name = self.driver.find_element(
            get_element("myFavorite_page", "product_goodsName_button_loc")).text
        self.driver.find_element(get_element("myFavorite_page", "product_goodsName_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "addFavorite_button_loc")).click()
        time.sleep(2)
        goods_favorite_status = self.driver.find_element(
            get_element("myFavorite_page", "addFavorite_status_text_loc")).text
        self.assertEqual("已收藏产品", goods_favorite_status, "商品收藏状态错误")
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        favorite_goods_name = self.driver.find_element(
            get_element("myFavorite_page", "myFavorite_goodsName_text_loc")).text
        self.assertIn(goods_name, favorite_goods_name, "商品详情页面-添加收藏夹失败")
        delete_sql = "DELETE FROM cenpur_mall_favorites where user_id = '26878e6d32df4e1c95b579af43990da4'"
        connect_sql(delete_sql)
    '''
    case：加入收藏夹-商品收藏-店铺详情页面
    expected：
    成功收藏商品
    '''
    def test_1_addFavorite_1_addGoods_2_shopDetail(self):
        self.driver.find_element(get_element("myFavorite_page", "product_goodsName_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("cart_page", "enterShop_button_loc")).click()
        time.sleep(2)
        shop_goods_list = self.driver.load_table(
            "cart_page", "shopDetail_goodsList_table_data_loc", "shopDetail_goodsList_table_name_loc")
        shop_goods_name_list = shop_goods_list["商品品名"]
        self.driver.find_element(get_element("cart_page", "shopDetail_addFavorite_button_loc")).click()
        self.driver.find_element(get_element("home_page", "shopDetail_member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        favorite_goods_name = self.driver.find_element(
            get_element("myFavorite_page", "myFavorite_goodsName_text_loc")).text
        self.assertIn(shop_goods_name_list[0], favorite_goods_name, "店铺详情页面-添加收藏夹失败")
    '''
    case：加入收藏夹-店铺收藏
    expected：
    成功收藏店铺
    '''
    def test_1_addFavorite_2_addShop_1_addFavorite(self):
        self.driver.find_element(get_element("myFavorite_page", "product_goodsName_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "addShop_button_loc")).click()
        time.sleep(2)
        shop_favorite_status = self.driver.find_element(get_element("myFavorite_page", "addShop_button_loc")).text
        self.assertEqual("已收藏", shop_favorite_status, "店铺收藏状态错误")
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        self.driver.find_element(get_element("myFavorite_page", "favoriteShop_tab_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("myFavorite_page", "favoriteShop_delete_button_loc")), "店铺收藏失败")
    '''
    case：加入收藏夹-店铺收藏-进入店铺详情页面
    expected：
    通过收藏店铺页面进入店铺详情页面
    '''
    def test_1_addFavorite_2_addShop_2_enterShopDetail(self):
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        self.driver.find_element(get_element("myFavorite_page", "favoriteShop_tab_loc")).click()
        self.driver.find_element(get_element("myFavorite_page", "favoriteShop_enterShopDetail_button_loc")).click()
        self.assertTrue(self.driver.is_element_exist(
            get_element("myFavorite_page", "shopDetail_goodsName_text_loc")), "收藏店铺-跳转店铺详情页面失败")
    '''
    case：加入收藏夹-删除-商品
    expected：
    收藏商品从收藏夹中移除
    '''
    def test_1_addFavorite_3_deleteFavorite_1_goods(self):
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "favoriteGoods_delete_button_loc")).click()
        time.sleep(2)
        self.assertFalse(self.driver.is_element_exist(
            get_element("myFavorite_page", "favoriteGoods_delete_button_loc")), "收藏夹商品删除失败")
    '''
    case：加入收藏夹-删除-店铺
    expected：
    收藏店铺从收藏夹中移除
    '''
    def test_1_addFavorite_3_deleteFavorite_2_shop(self):
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "favoriteShop_tab_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "favoriteShop_delete_button_loc")).click()
        time.sleep(2)
        self.assertFalse(self.driver.is_element_exist(
            get_element("myFavorite_page", "favoriteShop_delete_button_loc")), "收藏夹商品删除失败")
    '''
    case：收藏夹-加入购物车
    expected：
    收藏夹商品成功加入购物车
    '''
    def _2_toCart_1_addCart(self):
        goods_name = self.driver.find_element(
            get_element("myFavorite_page", "product_goodsName_button_loc")).text
        self.driver.find_element(get_element("myFavorite_page", "product_goodsName_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myFavorite_page", "addFavorite_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("home_page", "member_href_loc")).click()
        self.driver.find_element(get_element("member_page", "favorite_href_loc")).click()
        self.driver.find_element(get_element("myFavorite_page", "favoriteGoods_checkAll_checkbox_loc")).click()
        # test = self.driver.is_element_exist(get_element("myFavorite_page", "favoriteGoods_checkAll_checkbox_loc"))
        current_url = self.driver.get_current_url()
        self.driver.find_element(get_element("myFavorite_page", "addToCart_button_loc")).click()
        time.sleep(1)
        skip_url = self.driver.get_current_url()
        self.assertNotEqual(current_url, skip_url, "收藏夹页面跳转购物车页面失败")
        cart_goods_name = self.driver.find_element(get_element("cart_page", "cartGoods_name_text_loc")).text
        self.assertIn(goods_name, cart_goods_name, "商品详情页面-商品添加购物车失败")
        delete_cart_goods_sql = "DELETE FROM cenpur_mall_cart_goods where cart_id = (select id from " \
                                "cenpur_mall_cart where user_id = '26878e6d32df4e1c95b579af43990da4')"
        connect_sql(delete_cart_goods_sql)
        delete_favorite_goods_sql = "DELETE FROM cenpur_mall_favorites " \
                                    "where user_id = '26878e6d32df4e1c95b579af43990da4'"
        connect_sql(delete_favorite_goods_sql)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
