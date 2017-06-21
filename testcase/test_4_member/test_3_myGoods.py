# -*-coding:utf-8-*-
import time
import unittest
from pyse.init_pyse import Pyse
from testlibs.log import Logger
from utils.loadyaml import *
from utils.connectSQL import *

autolog = Logger()


class TestMyGoods(unittest.TestCase):

    def setUp(self):
        self.driver = Pyse('firefox')
        self.driver.open(get_url("home_page"))
        autolog.info("登录")
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
        self.driver.click(get_element("home_page", "member_href_loc"))
        self.driver.click(get_element("member_page", "myGoods_href_loc"))
        time.sleep(2)
    '''
    case：待提交商品-检查数据
    expected：
    正确加载待提交商品列表，商品信息正确显示
    '''
    def test_myGoods_1_draftGoods_1_data(self):
        autolog.info("切换到待提交商品页面")
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        # 数据库获取待提交商品信息
        draft_goods_sql = "select code,name,tagout_num,harbor,store,price_type,price from cenpur_mall_goods " \
                          "where shop_id = 2 and state = 0"
        sql_draft_goods_list = connect_sql(draft_goods_sql)
        # 获取数据库待提交商品编码列表
        sql_goods_num_list = []
        for i in sql_draft_goods_list:
            sql_goods_num_list.append(i[0])
        # 断言商品条数是否一致
        self.assertEqual(len(sql_goods_num_list), len(draft_goods_list["商品编号"]), "待提交商品列表加载失败")
        for i in draft_goods_list["状态"]:
            self.assertEqual("待提交", i, "商品状态错误")
    '''
    case：待提交商品-可用功能列表
    expected：
    待提交商品可用功能：查看，修改，删除，上架，复制挂牌
    '''
    def test_myGoods_1_draftGoods_2_option(self):
        autolog.info("切换到待提交商品页面")
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        print(draft_goods_list["操作"])
        self.assertIn("查看", draft_goods_list["操作"][0], "待提交商品缺少功能-查看")
        self.assertIn("修改", draft_goods_list["操作"][0], "待提交商品缺少功能-修改")
        self.assertIn("删除", draft_goods_list["操作"][0], "待提交商品缺少功能-删除")
        self.assertIn("上架", draft_goods_list["操作"][0], "待提交商品缺少功能-上架")
        self.assertIn("复制挂牌", draft_goods_list["操作"][0], "待提交商品缺少功能-复制挂牌")
        self.assertNotIn("下架", draft_goods_list["操作"][0], "待提交商品错误功能-下架")
        self.assertNotIn("暂停销售", draft_goods_list["操作"][0], "待提交商品错误功能-暂停销售")
        self.assertNotIn("继续销售", draft_goods_list["操作"][0], "待提交商品错误功能-继续销售")
    '''
    case：待提交商品-查看
    expected：
    跳转商品挂盘页面，商品信息无法编辑
    '''
    def test_myGoods_1_draftGoods_3_view(self):
        autolog.info("切换到待提交商品页面")
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        current_url = self.driver.get_current_url()
        autolog.info("查看商品")
        self.driver.find_element(get_element("myGoods_page", "goods_button1_loc")).click()
        skip_url = self.driver.get_current_url()
        self.assertNotEqual(current_url, skip_url, "点击查看，页面未跳转")
        goods_name_input = self.driver.find_element(get_element("myGoods_page", "goodsInfo_goodsName_input_loc"))
        goods_name_attr = goods_name_input.get_attribute("disabled")
        self.assertTrue(goods_name_attr, "商品查看页面，商品信息可编辑")
    '''
    case：待提交商品-编辑存草稿
    expected：
    跳转商品编辑页面，可以修改商品信息
    '''
    def test_myGoods_1_draftGoods_4_edit_draft(self):
        autolog.info("切换到待提交商品页面")
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        current_url = self.driver.get_current_url()
        autolog.info("修改商品")
        self.driver.find_element(get_element("myGoods_page", "goods_button2_loc")).click()
        time.sleep(1)
        skip_url = self.driver.get_current_url()
        self.assertNotEqual(current_url, skip_url, "点击修改，页面未跳转")
        goods_name_input = self.driver.find_element(get_element("myGoods_page", "goodsInfo_goodsName_input_loc"))
        goods_name_input.clear()
        autolog.info("修改商品名称：testEdit")
        goods_name_input.send_keys("testEdit")
        self.assertEqual("testEdit", goods_name_input.get_attribute("value"), "编辑商品名称失败")
        autolog.info("存草稿")
        self.driver.find_element(get_element("myGoods_page", "goodsInfo_draft_button_loc")).click()
        autolog.info("切换到待提交商品页面")
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        edit_draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        self.assertIn("testEdit", edit_draft_goods_list["商品名称"], "编辑商品保存失败")

    '''
    case：待提交商品-编辑上架
    expected：
    商品上架
    '''
    def test_myGoods_1_draftGoods_5_edit_sale(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_account_before = len(sale_goods_list_before["商品名称"])
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myGoods_page", "goods_button2_loc")).click()
        time.sleep(1)
        goods_name_input = self.driver.find_element(get_element("myGoods_page", "goodsInfo_goodsName_input_loc"))
        goods_name_input.clear()
        goods_name_input.send_keys("ForTest")
        self.assertEqual("ForTest", goods_name_input.get_attribute("value"), "编辑商品名称失败")
        self.driver.find_element(get_element("myGoods_page", "goodsInfo_sale_button_loc")).click()
        time.sleep(2)
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_after = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_account_after = len(sale_goods_list_after["商品名称"])
        self.assertEqual(sale_goods_account_before+1, sale_goods_account_after, "待提交商品列表加载错误")
        select_sql = "select state from cenpur_mall_goods where shop_id = 2 and name = 'ForTest'"
        goods_status = connect_sql(select_sql)
        self.assertEqual(1, goods_status[0][0], "商品状态错误")
        update_sql = "update cenpur_mall_goods set state = 0 where shop_id = 2 and name = 'ForTest'"
        connect_sql(update_sql)
    '''
    case：待提交商品-删除商品
    expected：
    删除后，商品列表中不显示该商品
    '''
    def test_myGoods_1_draftGoods_6_delete(self):
        all_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        all_goods_account_before = len(all_goods_list_before["商品名称"])
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        delete_goods_name = draft_goods_list_before["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button3_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "删除确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % delete_goods_name
        goods_status = connect_sql(select_sql)
        self.assertEqual(4, goods_status[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "allGoods_button_loc")).click()
        time.sleep(2)
        all_goods_list_after = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        all_goods_account_after = len(all_goods_list_after["商品名称"])
        self.assertEqual(all_goods_account_before - 1, all_goods_account_after, "所有商品列表商品总数有误")
        update_sql = "update cenpur_mall_goods set state = 0 where shop_id=2 and name='%s'" % delete_goods_name
        connect_sql(update_sql)
    '''
    case：待提交商品-复制挂牌
    expected：
    跳转商品编辑页面，存草稿新增一个待提交商品
    '''
    def test_myGoods_1_draftGoods_7_copy(self):
        pass
    '''
    case：待提交商品-上架商品
    expected：
    商品状态改变
    '''
    def test_myGoods_1_draftGoods_8_sale(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_accout_before = len(sale_goods_list_before["商品名称"])
        self.driver.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_name = draft_goods_list["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button4_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "上架确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % sale_goods_name
        goods_state = connect_sql(select_sql)
        self.assertEqual(1, goods_state[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_after = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_accout_after = len(sale_goods_list_after["商品名称"])
        self.assertEqual(sale_goods_accout_before+1, sale_goods_accout_after, "商品上架失败")
        update_sql = "update cenpur_mall_goods set state = 0 where shop_id=2 and name='%s'" % sale_goods_name
        connect_sql(update_sql)
    '''
    case：所有商品-检查数据
    expected：
    所有商品正确加载
    '''
    def test_myGoods_2_allGoods_1_data(self):
        all_goods_sql = "select code,name,tagout_num,harbor,store,price_type,price from cenpur_mall_goods " \
                          "where shop_id = 2 and state != 4"
        sql_all_goods_list = connect_sql(all_goods_sql)
        sql_all_goods_code_list = []
        for i in sql_all_goods_list:
            sql_all_goods_code_list.append(i[0])
        all_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        self.assertEqual(len(sql_all_goods_code_list), len(all_goods_list["商品编号"]), "所有商品列表加载失败")
    '''
    case：已上架商品-检查数据
    expected：
    正确加载已上架商品列表，商品信息正确显示
    '''
    def test_myGoods_3_saleGoods_1_data(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        # 数据库获取待提交商品信息
        draft_goods_sql = "select code,name,tagout_num,harbor,store,price_type,price from cenpur_mall_goods " \
                          "where shop_id = 2 and state = 1"
        sql_sale_goods_list = connect_sql(draft_goods_sql)
        # 获取数据库待提交商品编码列表
        sql_goods_num_list = []
        for i in sql_sale_goods_list:
            sql_goods_num_list.append(i[0])
        # 断言商品条数是否一致
        self.assertEqual(len(sql_goods_num_list), len(sale_goods_list["商品编号"]), "已上架商品列表加载失败")
        for i in sale_goods_list["状态"]:
            self.assertEqual("已上架", i, "商品状态错误")
    '''
    case：已上架商品-可用功能列表
    expected：
    已上架商品可用功能：查看，下架，暂停销售，复制挂牌
    '''
    def test_myGoods_3_saleGoods_2_option(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        print(draft_goods_list["操作"])
        self.assertIn("查看", draft_goods_list["操作"][0], "待提交商品缺少功能-查看")
        self.assertIn("下架", draft_goods_list["操作"][0], "待提交商品缺少功能-下架")
        self.assertIn("暂停销售", draft_goods_list["操作"][0], "待提交商品缺少功能-暂停销售")
        self.assertIn("复制挂牌", draft_goods_list["操作"][0], "待提交商品缺少功能-复制挂牌")
        self.assertNotIn("上架", draft_goods_list["操作"][0], "待提交商品错误功能-上架")
        self.assertNotIn("删除", draft_goods_list["操作"][0], "待提交商品错误功能-删除")
        self.assertNotIn("继续销售", draft_goods_list["操作"][0], "待提交商品错误功能-继续销售")
        self.assertNotIn("修改", draft_goods_list["操作"][0], "待提交商品错误功能-修改")
    '''
    case：已上架商品-查看
    expected：
    跳转商品挂盘页面，商品信息无法编辑
    '''
    def test_myGoods_3_saleGoods_3_view(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        current_url = self.driver.get_current_url()
        self.driver.find_element(get_element("myGoods_page", "goods_button1_loc")).click()
        skip_url = self.driver.get_current_url()
        self.assertNotEqual(current_url, skip_url, "点击查看，页面未跳转")
        goods_name_input = self.driver.find_element(get_element("myGoods_page", "goodsInfo_goodsName_input_loc"))
        input_attr = goods_name_input.get_attribute("disabled")
        self.assertTrue(input_attr, "商品查看页面，商品信息可编辑")
    '''
    case：已上架商品-暂停销售
    expected：
    商品状态变为已暂停
    '''
    def test_myGoods_3_saleGoods_4_pause(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        pause_goods_name = sale_goods_list_before["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button3_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "暂停销售确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        sale_goods_list_after = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        goods_name = sale_goods_list_after["商品名称"][0]
        self.assertNotEqual(pause_goods_name, goods_name, "商品暂停销售失败")
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % pause_goods_name
        goods_state = connect_sql(select_sql)
        self.assertEqual(2, goods_state[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "pauseGoods_button_loc")).click()
        time.sleep(2)
        pause_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        pause_goods_name_list = pause_goods_list["商品名称"]
        self.assertIn(pause_goods_name, pause_goods_name_list, "商品加入已暂停商品列表失败")
        update_sql = "update cenpur_mall_goods set state = 1 where shop_id=2 and name='%s'" % pause_goods_name
        connect_sql(update_sql)
    '''
    case：已上架商品-下架
    expected：
    商品状态变为已下架
    '''
    def test_myGoods_3_saleGoods_5_soldOut(self):
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sold_out_goods_name = sale_goods_list_before["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button2_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "商品下架确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % sold_out_goods_name
        goods_state = connect_sql(select_sql)
        self.assertEqual(3, goods_state[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "soldOutGoods_button_loc")).click()
        time.sleep(2)
        sold_out_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sold_out_goods_name_list = sold_out_goods_list["商品名称"]
        self.assertIn(sold_out_goods_name, sold_out_goods_name_list, "商品加入已下架商品列表失败")
        update_sql = "update cenpur_mall_goods set state = 1 where shop_id=2 and name='%s'" % sold_out_goods_name
        connect_sql(update_sql)
    '''
    case：已暂停商品-检查数据
    expected：
    正确加载已暂停商品列表，商品信息正确显示
    '''
    def test_myGoods_4_pauseGoods_1_data(self):
        self.driver.find_element(get_element("myGoods_page", "pauseGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        # 数据库获取待提交商品信息
        draft_goods_sql = "select code,name,tagout_num,harbor,store,price_type,price from cenpur_mall_goods " \
                          "where shop_id = 2 and state = 2"
        sql_sale_goods_list = connect_sql(draft_goods_sql)
        # 获取数据库待提交商品编码列表
        sql_goods_num_list = []
        for i in sql_sale_goods_list:
            sql_goods_num_list.append(i[0])
        # 断言商品条数是否一致
        self.assertEqual(len(sql_goods_num_list), len(sale_goods_list["商品编号"]), "已上架商品列表加载失败")
        for i in sale_goods_list["状态"]:
            self.assertEqual("已暂停", i, "商品状态错误")
    '''
    case：已暂停商品-可用功能列表
    expected：
    已暂停商品可用功能：查看，下架，继续销售，复制挂牌
    '''
    def test_myGoods_4_pauseGoods_2_option(self):
        self.driver.find_element(get_element("myGoods_page", "pauseGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        print(draft_goods_list["操作"])
        self.assertIn("查看", draft_goods_list["操作"][0], "待提交商品缺少功能-查看")
        self.assertIn("下架", draft_goods_list["操作"][0], "待提交商品缺少功能-下架")
        self.assertIn("继续销售", draft_goods_list["操作"][0], "待提交商品缺少功能-继续销售")
        self.assertIn("复制挂牌", draft_goods_list["操作"][0], "待提交商品缺少功能-复制挂牌")
        self.assertNotIn("上架", draft_goods_list["操作"][0], "待提交商品错误功能-上架")
        self.assertNotIn("暂停销售", draft_goods_list["操作"][0], "待提交商品错误功能-暂停销售")
        self.assertNotIn("修改", draft_goods_list["操作"][0], "待提交商品错误功能-修改")
        self.assertNotIn("删除", draft_goods_list["操作"][0], "待提交商品错误功能-删除")
    '''
    case：已暂停商品-下架商品
    expected：
    商品状态改变，加入已下架列表
    '''
    def test_myGoods_4_pauseGoods_3_soldOut(self):
        self.driver.find_element(get_element("myGoods_page", "pauseGoods_button_loc")).click()
        time.sleep(2)
        pause_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sold_out_goods_name = pause_goods_list_before["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button2_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "商品下架确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % sold_out_goods_name
        goods_state = connect_sql(select_sql)
        self.assertEqual(3, goods_state[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "soldOutGoods_button_loc")).click()
        time.sleep(2)
        sold_out_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sold_out_goods_name_list = sold_out_goods_list["商品名称"]
        self.assertIn(sold_out_goods_name, sold_out_goods_name_list, "商品加入已下架商品列表失败")
        update_sql = "update cenpur_mall_goods set state = 2 where shop_id=2 and name='%s'" % sold_out_goods_name
        connect_sql(update_sql)
    '''
    case：已暂停商品-商品继续销售
    expected：
    商品状态改变，加入已上架列表
    '''
    def test_myGoods_4_pauseGoods_4_keepSale(self):
        self.driver.find_element(get_element("myGoods_page", "pauseGoods_button_loc")).click()
        time.sleep(2)
        pause_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_name = pause_goods_list_before["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button3_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "商品继续销售确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % sale_goods_name
        goods_state = connect_sql(select_sql)
        self.assertEqual(1, goods_state[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "saleGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        sale_goods_name_list = sale_goods_list["商品名称"]
        self.assertIn(sale_goods_name, sale_goods_name_list, "商品加入已上架商品列表失败")
        update_sql = "update cenpur_mall_goods set state = 2 where shop_id=2 and name='%s'" % sale_goods_name
        connect_sql(update_sql)
    '''
     case：已下架商品-检查数据
     expected：
     正确加载已下架商品列表，商品信息正确显示
     '''
    def test_myGoods_5_soldOutGoods_1_data(self):
        self.driver.find_element(get_element("myGoods_page", "soldOutGoods_button_loc")).click()
        time.sleep(2)
        sale_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        # 数据库获取待提交商品信息
        draft_goods_sql = "select code,name,tagout_num,harbor,store,price_type,price from cenpur_mall_goods " \
                          "where shop_id = 2 and state = 1"
        sql_sale_goods_list = connect_sql(draft_goods_sql)
        # 获取数据库待提交商品编码列表
        sql_goods_num_list = []
        for i in sql_sale_goods_list:
            sql_goods_num_list.append(i[0])
        # 断言商品条数是否一致
        self.assertEqual(len(sql_goods_num_list), len(sale_goods_list["商品编号"]), "已下架商品列表加载失败")
        for i in sale_goods_list["状态"]:
            self.assertEqual("已下架", i, "商品状态错误")
    '''
    case：已下架商品-可用功能列表
    expected：
    已下架商品可用功能：查看，删除，复制挂牌
    '''
    def test_myGoods_5_soldOutGoods_2_option(self):
        self.driver.find_element(get_element("myGoods_page", "soldOutGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        print(draft_goods_list["操作"])
        self.assertIn("查看", draft_goods_list["操作"][0], "待提交商品缺少功能-查看")
        self.assertIn("删除", draft_goods_list["操作"][0], "待提交商品缺少功能-删除")
        self.assertIn("复制挂牌", draft_goods_list["操作"][0], "待提交商品缺少功能-复制挂牌")
        self.assertNotIn("修改", draft_goods_list["操作"][0], "待提交商品错误功能-修改")
        self.assertNotIn("上架", draft_goods_list["操作"][0], "待提交商品错误功能-上架")
        self.assertNotIn("下架", draft_goods_list["操作"][0], "待提交商品错误功能-下架")
        self.assertNotIn("暂停销售", draft_goods_list["操作"][0], "待提交商品错误功能-暂停销售")
        self.assertNotIn("继续销售", draft_goods_list["操作"][0], "待提交商品错误功能-继续销售")
    '''
    case：已下架商品-删除商品
    expected：
    商品删除后，不再在商品列表中显示
    '''
    def test_myGoods_5_soldOutGoods_2_delete(self):
        all_goods_list_before = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        all_goods_account_before = len(all_goods_list_before["商品名称"])
        self.driver.find_element(get_element("myGoods_page", "soldOutGoods_button_loc")).click()
        time.sleep(2)
        sold_out_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        delete_goods_name = sold_out_goods_list["商品名称"][0]
        self.driver.find_element(get_element("myGoods_page", "goods_button2_loc")).click()
        button_status = self.driver.is_element_exist(get_element("myGoods_page", "confirm_button_loc"))
        self.assertTrue(button_status, "删除确认窗口未弹出")
        self.driver.find_element(get_element("myGoods_page", "confirm_button_loc")).click()
        time.sleep(2)
        select_sql = "select state from cenpur_mall_goods where shop_id=2 and name='%s'" % delete_goods_name
        goods_status = connect_sql(select_sql)
        self.assertEqual(4, goods_status[0][0], "商品状态错误")
        self.driver.find_element(get_element("myGoods_page", "allGoods_button_loc")).click()
        time.sleep(2)
        all_goods_list_after = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        all_goods_account_after = len(all_goods_list_after["商品名称"])
        self.assertEqual(all_goods_account_before-1, all_goods_account_after, "所有商品列表商品总数有误")
        update_sql = "update cenpur_mall_goods set state = 0 where shop_id=2 and name='%s'" % delete_goods_name
        connect_sql(update_sql)
    '''
    case：其他-搜索商品
    expected：
    根据搜索关键字显示商品列表
    '''
    def test_myGoods_6_other_1_searchByKey(self):
        all_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        all_goods_name_list = all_goods_list["商品名称"]
        self.driver.find_element(get_element("myGoods_page", "selectGoods_input_loc")).send_keys("ForTest")
        self.driver.find_element(get_element("myGoods_page", "selectGoods_button_loc")).click()
        time.sleep(2)
        search_goods_list = self.driver.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        search_goods_name_list = search_goods_list["商品名称"]
        for i in search_goods_name_list:
            self.assertIn(i, all_goods_name_list, "搜索结果显示错误")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
