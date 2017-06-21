# -*-coding:utf-8-*-
import time
import unittest
from pyse.init_pyse import Pyse
from testlibs.log import Logger
from utils.loadyaml import *

autolog = Logger()


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.page_name = "login_page"
        self.login = Pyse('chrome')
        self.login.open(get_url("home_page"))

    '''
    case：用户登录-正确登录
    1.正确匹配的用户名、密码
    2.登录跳转
    expected:
    登录成功，跳转首页
    '''
    def test_1_login_1_normal(self):
        self.login.click(get_element("login_page", "switch_button_loc"))
        autolog.info("弹出登录窗口")
        current_handle = self.login.switch_window()
        autolog.info("输入用户名：")
        self.login.send_keys(get_element("login_page", "username_input_loc"), "15881122294")
        autolog.info("输入密码：")
        self.login.send_keys(get_element("login_page", "password_input_loc"), "Xian1016")
        autolog.info("输入验证码：")
        self.login.send_keys(get_element("login_page", "verifyCode_input_loc"), "8888")
        autolog.info("确认登录")
        self.login.click(get_element("login_page", "login_button_loc"))
        time.sleep(2)
        result_handle = self.login.all_window_handles()
        self.assertNotIn(current_handle, result_handle, "登录失败，登录窗口未关闭！")
        self.login.switch_to_single_window()
    '''
    case：用户登录-必填项验证
    1.用户名、密码分别为空
    2.用户名、密码同时为空
    expected：
    登录失败，显示对应提示信息
    '''
    # def test_1_login_2_required(self):

    '''
    case：用户登录-无效用户名或密码
    1、错误用户名
    2.错误密码
    expected：
    登录失败，显示对应提示信息
    '''
    # def test_1_login_3_invalid(self):

    '''
    case：用户登录-自动登录
    1.正确登录
    2.二次登录验证
    expected：
    二次登录时自动登录成功
    '''
    # def test_1_login_4_auto_login(self):

    def tearDown(self):
        self.login.quit()
