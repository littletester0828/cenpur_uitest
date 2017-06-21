# -*- coding:utf-8 -*-

import sys
from testlibs.log import Logger
from pyse.init_pyse import Pyse

sys.path.append('../')
autolog = Logger()
login_testurl = "http://222.209.88.121:9999/zlgxjy/member/login.html"
login_url = "https://dsjk.zsteel.cc/zlgxjy/member/login.html"


class LoginPage(Pyse):
    # 定位器，定位页面元素
    username_loc = ("id", "loginname")
    password_loc = ("id", "password")
    vcode_loc = ("id", "vcode")
    remeber_loc = ('id', 'northRemeber')
    login_loc = ("xpath", "/html/body/div[2]/div/div[2]/div[4]/input")
    error_loc = ("xpath", "//*[@id=\"error\"]/div/label")
    success_loc = ("xpath", "/html/body/div[1]/div/ul/li[5]/h6/a")
    logout_loc = ("xpath", "/html/body/div[1]/div/ul/li[7]/h6/a")
    forgotpsw_loc = ("xpath", "/html/body/div[2]/div/div[2]/div[3]/div[4]/ul/li[2]/a")

    def input_username(self, username):
        autolog.info("输入用户名：" + username)
        # 输入账号框
        self.send_keys(self.username_loc, username)

    def input_password(self, password):
        autolog.info("输入密码：" + password)
        # 输入密码框
        self.send_keys(self.password_loc, password)

    def click_login(self):
        # 登录按钮
        self.click(self.login_loc)
