# -*-coding:utf-8-*-
import time
import unittest
from pyse.init_pyse import Pyse
from testlibs.log import Logger
from utils.loadyaml import *
from utils.connectSQL import *

autolog = Logger()


class TestAddGoods(unittest.TestCase):

    def setUp(self):
        self.login = Pyse('chrome')
        self.login.open(get_url("home_page"))
        self.login.click(get_element("login_page", "switch_button_loc"))
        current_handle = self.login.switch_window()
        self.login.send_keys(get_element("login_page", "username_input_loc"), "15881122294")
        self.login.send_keys(get_element("login_page", "password_input_loc"), "Xian1016")
        self.login.send_keys(get_element("login_page", "verifyCode_input_loc"), "8888")
        self.login.click(get_element("login_page", "login_button_loc"))
        time.sleep(2)
        result_handle = self.login.all_window_handles()
        self.assertNotIn(current_handle, result_handle, "登录失败，登录窗口未关闭！")
        self.login.switch_to_single_window()
        self.login.click(get_element("home_page", "member_href_loc"))
        self.login.click(get_element("member_page", "addGoods_href_loc"))
        time.sleep(2)
    '''
    case：商品挂盘-入口验证
    我的商品-商品挂盘按钮
    expected：
    成功跳转商品挂盘编辑页面
    '''
    def test_addGoods_1_entry_1_myGoods(self):
        autolog.info("跳转我的商品页面")
        time.sleep(2)
        self.login.click(get_element("member_page", "myGoods_href_loc"))
        time.sleep(2)
        self.assertEqual(get_url("goods_page"), self.login.get_current_url(), "跳转我的商品页面失败！")
        autolog.info("我的商品跳转商品挂盘页面")
        self.login.click(get_element("myGoods_page", "addGoods_button_loc"))
        self.assertEqual(get_url("addGoods_page"), self.login.get_current_url(), "跳转商品挂盘页面失败！")
    '''
    case：商品挂盘-入口验证
    会员中心导航栏-商品挂盘
    expected：
    成功跳转商品挂盘编辑页面
    '''
    def test_addGoods_1_entry_2_addGoods(self):
        autolog.info("跳转我的商品页面")
        time.sleep(2)
        self.login.click(get_element("member_page", "myGoods_href_loc"))
        time.sleep(2)
        autolog.info("会员中心导航栏跳转商品挂盘页面")
        self.login.click(get_element("member_page", "addGoods_href_loc"))
        self.assertEqual(get_url("addGoods_page"), self.login.get_current_url(), "跳转商品挂盘页面失败！")
    '''
    case：商品挂盘-新增-提交表单
    1.挂盘方式
    2.商品类型、船名、商品大类、指标类型、品质指标、产地、币种、商品名、溢短装
    3.截止日期
    4.商品价格、计价方式、发盘量、起订量
    5、支付方式、付款时间、港口或仓库、商品图片上传
    6、后台数据库查询新增商品数据
    expected：
    后台数据库数据新增成功，商品挂盘成功
    '''
    def test_addGoods_1_submit(self):
        ship_name = "珍珠号"
        goods_name = "OnlyTest"
        time.sleep(2)
        self.login.click(get_element("member_page", "addGoods_href_loc"))
        # 选择挂盘方式-普通挂盘
        common_radio = self.login.find_element(get_element("addGoods_page", "commonAdd_radio_loc"))
        autolog.info("选择挂盘方式-普通挂盘")
        common_radio.click()
        add_type_is_selected = common_radio.is_selected()
        self.assertTrue(add_type_is_selected, "挂盘方式-普通挂盘选中失败！")
        # 选择商品类型-现货
        actuals_radio = self.login.find_element(get_element("addGoods_page", "actuals_radio_loc"))
        autolog.info("选择商品类型-现货")
        actuals_radio.click()
        goodstype_is_selected = actuals_radio.is_selected()
        self.assertTrue(goodstype_is_selected, "商品类型-现货选中失败！")
        # 填写船名：ship_name
        boat_name_text = self.login.find_element(get_element("addGoods_page", "shipName_input_loc"))
        autolog.info("填写船名：" + ship_name)
        boat_name_text.send_keys(ship_name)
        self.assertEqual(ship_name, boat_name_text.get_attribute("value"), "船名填写失败！")
        # 选择商品大类-铁矿
        iron_ore_radio = self.login.find_element(get_element("addGoods_page", "ironOre_radio_loc"))
        autolog.info("选择商品大类-铁矿")
        iron_ore_radio.click()
        goods_category_is_selected = iron_ore_radio.is_selected()
        self.assertTrue(goods_category_is_selected, "商品大类-铁矿选中失败！")
        # 填写品质指标
        Fe_text = self.login.find_element(get_element("addGoods_page", "Fe_input_loc"))
        autolog.info("填写Fe：600")
        Fe_text.send_keys("600")
        self.assertEqual("600", Fe_text.get_attribute("value"), "Fe填写失败！")
        SiO2_text = self.login.find_element(get_element("addGoods_page", "SiO2_input_loc"))
        autolog.info("填写SiO2：20")
        SiO2_text.send_keys("20")
        self.assertEqual("20", SiO2_text.get_attribute("value"), "SiO2填写失败！")
        AI2O3_text = self.login.find_element(get_element("addGoods_page", "AI2O3_input_loc"))
        autolog.info("填写AI2O3：50")
        AI2O3_text.send_keys("50")
        self.assertEqual("50", AI2O3_text.get_attribute("value"), "AI2O3填写失败！")
        S_text = self.login.find_element(get_element("addGoods_page", "S_input_loc"))
        autolog.info("填写S：60")
        S_text.send_keys("60")
        self.assertEqual("60", S_text.get_attribute("value"), "S填写失败！")
        H2O_text = self.login.find_element(get_element("addGoods_page", "H2O_input_loc"))
        autolog.info("填写H2O：50")
        H2O_text.send_keys("50")
        self.assertEqual("50", H2O_text.get_attribute("value"), "H2O填写失败！")
        FeO_text = self.login.find_element(get_element("addGoods_page", "FeO_input_loc"))
        autolog.info("填写FeO：70")
        FeO_text.send_keys("70")
        self.assertEqual("70", FeO_text.get_attribute("value"), "FeO填写失败！")
        P_text = self.login.find_element(get_element("addGoods_page", "P_input_loc"))
        autolog.info("填写P：50")
        P_text.send_keys("50")
        self.assertEqual("50", P_text.get_attribute("value"), "P填写失败！")
        Grade_text = self.login.find_element(get_element("addGoods_page", "Grade_input_loc"))
        autolog.info("填写粒度指标：50")
        Grade_text.send_keys("50")
        self.assertEqual("50", Grade_text.get_attribute("value"), "粒度指标填写失败！")
        # 填写商品名：goods_name
        goods_name_text = self.login.find_element(get_element("addGoods_page", "goodsName_input_loc"))
        autolog.info("填写商品名：" + goods_name)
        goods_name_text.send_keys(goods_name)
        self.assertEqual(goods_name, goods_name_text.get_attribute("value"), "商品名填写失败！")
        # 填写溢短装比例：10%
        more_or_less_text = self.login.find_element(get_element("addGoods_page", "moreOrLess_input_loc"))
        autolog.info("填写溢短装比例：" + "10%")
        more_or_less_text.send_keys("10%")
        self.assertEqual("10%", more_or_less_text.get_attribute("value"), "溢短装比例填写失败！")
        # 填写截止日期：Today
        today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        end_time_text = self.login.find_element(get_element("addGoods_page", "endTime_input_loc"))
        end_time_text.click()
        time.sleep(2)
        autolog.info("填写截止日期：" + today_time)
        self.login.find_element(get_element("addGoods_page", "endTime_button_loc")).click()
        self.assertEqual(today_time, end_time_text.get_attribute("value"), "截止时间填写失败！")
        # 填写商品价格：20
        goods_price_text = self.login.find_element(get_element("addGoods_page", "goodsPrice_input_loc"))
        autolog.info("填写商品价格：" + "20")
        goods_price_text.send_keys("20")
        self.assertEqual("20", goods_price_text.get_attribute("value"), "商品价格填写失败！")
        # 填写发盘量：5000
        stock_text = self.login.find_element(get_element("addGoods_page", "stock_input_loc"))
        autolog.info("填写发盘量：" + "5000")
        stock_text.send_keys("5000")
        self.assertEqual("5000", stock_text.get_attribute("value"), "发盘量填写失败！")
        # 填写起订量：200
        mini_order_text = self.login.find_element(get_element("addGoods_page", "miniOrder_input_loc"))
        autolog.info("填写发盘量：" + "200")
        mini_order_text.send_keys("200")
        self.assertEqual("200", mini_order_text.get_attribute("value"), "发盘量填写失败！")
        # 选择支付方式-在线支付
        pay_online_checkbox = self.login.find_element(get_element("addGoods_page", "payOnline_checkbox_loc"))
        autolog.info("选择支付方式-在线支付")
        pay_online_checkbox.click()
        pay_online_is_selected = pay_online_checkbox.is_selected()
        self.assertTrue(pay_online_is_selected, "选择支付方式-在线支付选中失败！")
        # 选择付款时间-分期付款
        pay_advance_checkbox = self.login.find_element(get_element("addGoods_page", "payAdvance_checkbox_loc"))
        autolog.info("选择付款时间-分期付款")
        pay_advance_checkbox.click()
        pay_advance_is_selected = pay_advance_checkbox.is_selected()
        self.assertTrue(pay_advance_is_selected, "选择付款时间-分期付款选中失败！")
        # 选择港口或仓库-港口
        port_radio = self.login.find_element(get_element("addGoods_page", "port_radio_loc"))
        autolog.info("选择港口或仓库-港口")
        port_radio.click()
        port_is_selected = port_radio.is_selected()
        self.assertTrue(port_is_selected, "选择港口或仓库-港口选中失败！")
        # 上传商品图片
        autolog.info("上传商品图片：")
        upload_file = self.login.find_element(get_element("addGoods_page", "uploadPic_file_loc"))
        upload_file.send_keys("D:\\3、Work\\bdfintAutoTest\\pic\\1.jpg")
        time.sleep(2)
        status = self.login.is_element_exist(get_element("addGoods_page", "uploadPic_review_button_loc"))
        self.assertTrue(status, "图片上传失败")
        autolog.info("预览上传图片")
        self.login.find_element(get_element("addGoods_page", "uploadPic_review_button_loc")).click()
        self.login.find_element(get_element("addGoods_page", "uploadPic_review_close_button_loc")).click()
        time.sleep(2)
        autolog.info("删除上传图片：")
        self.login.find_element(get_element("addGoods_page", "uploadPic_delete_button_loc")).click()
        autolog.info("再次上传商品图片：")
        upload_file = self.login.find_element(get_element("addGoods_page", "uploadPic_file_loc"))
        upload_file.send_keys("D:\\3、Work\\bdfintAutoTest\\pic\\1.jpg")
        time.sleep(2)
        status = self.login.is_element_exist(get_element("addGoods_page", "uploadPic_review_button_loc"))
        self.assertTrue(status, "图片上传失败")
        # 提交表单
        autolog.info("商品存草稿：")
        self.login.click(get_element("addGoods_page", "draft_button_loc"))
        time.sleep(2)
        # 查询数据库，验证数据插入情况
        sql = "select name,state from cenpur_mall_goods where shop_id = 2 and name = 'OnlyTest'"
        added_goods_status = connect_sql(sql)
        print(added_goods_status)
        self.assertNotEqual(0, len(added_goods_status), "新增商品插入数据库失败")
        # status：0-待提交
        self.assertEqual(0, added_goods_status[0][1], "商品状态错误")
        # 验证前端新增商品显示情况
        autolog.info("切换至待提交商品页面")
        self.login.find_element(get_element("myGoods_page", "draftGoods_button_loc")).click()
        time.sleep(2)
        draft_goods_list = self.login.load_table(
            "myGoods_page", "myGoods_table_data_loc", "myGoods_table_name_loc")
        self.assertIn(goods_name, draft_goods_list['商品名称'], "新增商品存草稿失败")
        delete_sql = "delete from cenpur_mall_goods where shop_id = 2 and name = '%s'" % goods_name
        connect_sql(delete_sql)
    '''
    case：商品挂盘-新增-表单必填项验证-船名
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_1_shipName(self):
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        result_before = self.login.is_element_exist(get_element("addGoods_page", "shipName_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-船名")
        autolog.info("填写船名：小螺号")
        self.login.find_element(get_element("addGoods_page", "shipName_input_loc")).send_keys("小螺号")
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "shipName_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-船名")
    '''
    case：商品挂盘-新增-表单必填项验证-商品名
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_2_goodsName(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "goodsName_text_loc"))
        autolog.info("填写商品名称：HelloWorld")
        self.assertEqual(True, result_before, "必填项提示信息未显示-商品名")
        self.login.find_element(get_element("addGoods_page", "goodsName_input_loc")).send_keys("HelloWorld")
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "goodsName_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-商品名")
    '''
    case：商品挂盘-新增-表单必填项验证-商品价格
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_3_goodsPrice(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "goodsPrice_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-商品价格")
        autolog.info("填写商品价格：20")
        self.login.find_element(get_element("addGoods_page", "goodsPrice_input_loc")).send_keys("20")
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "goodsPrice_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-商品价格")
    '''
    case：商品挂盘-新增-表单必填项验证-发盘量
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_4_stock(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "stock_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-发盘量")
        autolog.info("填写商品发盘量：5000")
        self.login.find_element(get_element("addGoods_page", "stock_input_loc")).send_keys("5000")
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "stock_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-发盘量")
    '''
    case：商品挂盘-新增-表单必填项验证-起订量
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_5_miniOrder(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "miniOrder_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-起订量")
        autolog.info("填写商品起订量：100")
        self.login.find_element(get_element("addGoods_page", "miniOrder_input_loc")).send_keys("100")
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "miniOrder_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-起订量")
    '''
    case：商品挂盘-新增-表单必填项验证-支付方式
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_6_payType(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "payType_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-支付方式")
        autolog.info("选择商品支付方式：在线支付")
        self.login.click(get_element("addGoods_page", "payOnline_checkbox_loc"))
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "payType_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-支付方式")
    '''
    case：商品挂盘-新增-表单必填项验证-支付时间
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_7_payTime(self):
        autolog.info("挂盘商品提交")
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        result_before = self.login.is_element_exist(get_element("addGoods_page", "payTime_text_loc"))
        self.assertEqual(True, result_before, "必填项提示信息未显示-支付时间")
        autolog.info("选择支付时间：分期付款")
        self.login.click(get_element("addGoods_page", "payAdvance_checkbox_loc"))
        autolog.info("挂盘商品提交")
        self.login.find_element(get_element("addGoods_page", "submit_button_loc")).click()
        time.sleep(2)
        result_after = self.login.is_element_exist(get_element("addGoods_page", "payTime_text_loc"))
        self.assertEqual(False, result_after, "必填项提示信息显示错误-支付时间")
    '''
    case：商品挂盘-新增-表单必填项验证-截止时间
    expected：
    表单填写不全，提交失败
    '''
    def test_addGoods_2_required_8_endTime(self):
        self.login.find_element(get_element("addGoods_page", "shipName_input_loc")).send_keys("TestTime")
        self.login.find_element(get_element("addGoods_page", "ironOre_radio_loc")).click()
        self.login.find_element(get_element("addGoods_page", "Fe_input_loc")).send_keys("30")
        self.login.find_element(get_element("addGoods_page", "SiO2_input_loc")).send_keys("20")
        self.login.find_element(get_element("addGoods_page", "AI2O3_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "S_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "P_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "H2O_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "FeO_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "Grade_input_loc")).send_keys("50")
        self.login.find_element(get_element("addGoods_page", "goodsName_input_loc")).send_keys("HelloWorld")
        self.login.find_element(get_element("addGoods_page", "goodsPrice_input_loc")).send_keys("20")
        self.login.find_element(get_element("addGoods_page", "stock_input_loc")).send_keys("5000")
        self.login.find_element(get_element("addGoods_page", "miniOrder_input_loc")).send_keys("100")
        self.login.find_element(get_element("addGoods_page", "payOnline_checkbox_loc")).click()
        self.login.find_element(get_element("addGoods_page", "payAdvance_checkbox_loc")).click()
        submit_before_url = self.login.get_current_url()
        # 提交表单
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        submit_after_url = self.login.get_current_url()
        self.assertEqual(submit_before_url, submit_after_url, "页面跳转，必填项未做限制-截止时间")
        autolog.info("选择截止时间：今天")
        self.login.find_element(get_element("addGoods_page", "endTime_input_loc")).click()
        time.sleep(2)
        self.login.find_element(get_element("addGoods_page", "endTime_button_loc")).click()
        self.login.click(get_element("addGoods_page", "submit_button_loc"))
        time.sleep(2)
        submit_after_url2 = self.login.get_current_url()
        self.assertNotEqual(submit_after_url, submit_after_url2, "页面未跳转，提交表单失败")
        delete_sql = "delete from cenpur_mall_goods where name = 'TestTime'"
        connect_sql(delete_sql)
    '''
    case：商品挂盘-新增-期货
    expected：
    期货对应的属性正确显示：装船期、预计离港日、预计到港日、提单日
    '''
    def test_addGoods_3_other_1_futures(self):
        autolog.info("选择商品类型：期货")
        self.login.find_element(get_element("addGoods_page", "futures_radio_loc")).click()
        start_time_status = self.login.is_element_exist(get_element("addGoods_page", "shipment_startTime_input_loc"))
        futures_text_status = self.login.is_element_exist(get_element("addGoods_page", "futures_text_loc"))
        self.assertTrue(start_time_status, "装船期开始时间不显示")
        self.assertTrue(futures_text_status, "必填项提示文本未显示")
    '''
    case：商品挂盘-新增-币种与商品价格单位关联
    expected：
    当币种变化时，商品价格单位自动关联变化
    '''
    def test_addGoods_3_other_2_currency(self):
        current_text = self.login.find_element(get_element("addGoods_page", "currency_input_loc")).text
        price_num_text_before = self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_input_loc")).text
        autolog.info("选择币种：美元")
        self.login.find_element(get_element("addGoods_page", "currency_input_loc")).click()
        self.login.find_element(get_element("addGoods_page", "currency_select_loc")).click()
        choose_text = self.login.find_element(get_element("addGoods_page", "currency_input_loc")).text
        self.assertNotEqual(current_text, choose_text, "币种选择失败")
        price_num_text_after = self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_input_loc")).text
        self.assertNotEqual(price_num_text_before, price_num_text_after, "商品价格单位与币种关联失败")
    '''
    case：商品挂盘-新增-商品价格单位与发盘量、起订量单位关联
    expected：
    当商品价格单位变化时，发盘量和起订量单位自动关联变化
    '''
    def test_addGoods_3_other_3_priceNum(self):
        price_num_text_before = self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_input_loc")).text
        stock_num_text_before = self.login.find_element(get_element("addGoods_page", "stockNum_text_loc")).text
        mini_order_num_text_before = self.login.find_element(get_element("addGoods_page", "miniOrderNum_text_loc")).text
        autolog.info("选择商品价格单位：美元/湿吨")
        self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_input_loc")).click()
        self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_select_loc")).click()
        price_num_text_after = self.login.find_element(get_element("addGoods_page", "goodsPriceUnit_input_loc")).text
        self.assertNotEqual(price_num_text_before, price_num_text_after, "商品价格单位选择失败")
        stock_num_text_after = self.login.find_element(get_element("addGoods_page", "stockNum_text_loc")).text
        mini_order_num_text_after = self.login.find_element(get_element("addGoods_page", "miniOrderNum_text_loc")).text
        self.assertNotEqual(stock_num_text_before, stock_num_text_after, "发盘量单位关联失败")
        self.assertNotEqual(mini_order_num_text_before, mini_order_num_text_after, "起订量单位关联失败")
    '''
    case：商品挂盘-新增-无收货地址时新增地址
    expected：
    新增地址按钮，新增地址弹窗
    '''
    def test_addGoods_3_other_4_addAddress(self):
        delete_sql = "delete from cenpur_user_address " \
                     "where user_id='26878e6d32df4e1c95b579af43990da4' and address_type=2"
        connect_sql(delete_sql)
        autolog.info("选择仓库")
        self.login.find_element(get_element("addGoods_page", "depot_radio_loc")).click()
        add_address_button_status = self.login.is_element_exist(get_element(
            "addGoods_page", "depot_addAddress_button_loc"))
        self.assertTrue(add_address_button_status, "添加地址按钮不显示")
        autolog.info("添加发货地址")
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_button_loc")).click()
        add_address_window_status = self.login.is_element_exist(get_element(
            "addGoods_page", "depot_addAddress_window_loc"))
        self.assertTrue(add_address_window_status, "添加地址窗口未弹出")
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_consignor_input_loc")).send_keys(
            "测试专用")
        detail_address = "天府广场东侧速8酒店12层"
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_detail_input_loc")).send_keys(
            detail_address)
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_companyName_input_loc")).send_keys(
            "Tencent")
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_depot_input_loc")).send_keys("成都港")
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_contact_input_loc")).send_keys("110")
        autolog.info("发货地址提交")
        self.login.find_element(get_element("addGoods_page", "depot_addAddress_confirm_button_loc")).click()
        time.sleep(2)
        add_address_window_status = self.login.is_element_exist(get_element(
            "addGoods_page", "depot_addAddress_window_loc"))
        self.assertFalse(add_address_window_status, "添加地址窗口未关闭")
        address_status = self.login.is_element_exist(get_element("addGoods_page", "depot_addressList_first_loc"))
        self.assertTrue(address_status, "加载收货地址失败")
        connect_sql(delete_sql)

    def tearDown(self):
        self.login.quit()

if __name__ == "__main__":
    unittest.main()
