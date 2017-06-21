# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.screenshot import pictureshoot
import sys
import time
from imp import reload
from utils.loadyaml import get_element

reload(sys)
# sys.setdefaultencoding('utf-8')


class Pyse(object):
    """
    基于原生的selenium框架做了二次封装.
    """
    def __init__(self, browser):
        """
         启动浏览器参数化，默认启动chrome.
        """
        self.driver = None
        if browser == "chrome" or "Chrome":
            self.driver = webdriver.Chrome()
        elif browser == "firefox" or "Firefox":
            self.driver = webdriver.Firefox()
        elif browser == "ie":
            self.driver = webdriver.Ie()
        else:
            print("请重新输入浏览器参数，比如：chrome或者firefox或者ie")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def get_driver(self):
        return self.driver

    def open(self, url, t='', timeout=10):
        '''
        使用get打开url后，判断title符合预期
        Usage:
        driver = Pyse()
        driver.open(url,t='')
        '''
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(t))
        except TimeoutException:
            pictureshoot()
            print("open %s title error" % url)
        except Exception as msg:
            pictureshoot()
            print("Error:%s" % msg)

    def find_element(self, locator):
        '''
        定位元素，参数locator是元祖类型
        Usage:
        locator = ("id","xxx")
        driver.find_element(locator)
        '''
        element = self.driver.find_element(locator[0], locator[1])
        return element

    def find_elements(self, locator):
        elements = self.driver.find_elements(locator[0], locator[1])
        return elements

    def find_element_by_css_selector(self, locator):
        element = self.driver.find_element_by_css_selector(locator[1])
        return element

    def find_element_by_class_name(self, locator):
        element = self.driver.find_element_by_class_name(locator[1])
        return element

    def click(self, locator):
        '''
        点击操作
        Usage:
        locator = ("id","xxx")
        driver.click(locator)
        '''
        element = self.find_element(locator)
        element.click()

    def send_keys(self, locator, text):
        '''
        发送文本，清空后输入
        Usage:
        locator = ("id","xxx")
        driver.send_keys(locator, text)
        '''
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def text_in_element(self, locator, text, timeout=10):
        '''
        判断文本在元素里,没定位到元素返回False
        result = driver.text_in_element(locator, text)
        '''
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print("元素没定位到：" + str(locator) + "or 链接超时，请检查网络")
            return False
        else:
            return result

    def move_to_element(self, locator):
        '''
        鼠标悬停操作
        Usage:
        locator = ("id","xxx")
        driver.move_to_element(locator)
        '''
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def drag_to_element(self, locator1, locator2):
        '''
        鼠标悬停操作
        Usage:
        locator = ("id","xxx")
        driver.move_to_element(locator)
        '''
        element = self.find_element(locator1)
        target = self.find_element(locator2)
        ActionChains(self.driver).drag_and_drop(element,target).perform()

    def back(self):
        """
        前进页面操作
        Usage:
        driver.back()
        """
        self.driver.back()

    def forward(self):
        """
        后退页面操作
        Usage:
        driver.forward()
        """
        self.driver.forward()

    def close(self):
        """
        关闭当前页签
        Usage:
        driver.close()
        """
        self.driver.close()

    def quit(self):
        """
        退出驱动并关闭浏览器
        Usage:
        driver.quit()
        """
        self.driver.quit()

    def refresh(self):
        """
        退出驱动并关闭浏览器
        Usage:
        driver.quit()
        """
        self.driver.refresh()

    def scroll_to_low(self):
        '''
        移动到浏览器底端 
        '''
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def get_title(self):
        return self.driver.title

    def is_element_exist(self, element_name):
        try:
            self.find_element(element_name)
        except NoSuchElementException as e:
            return False
        return True

    def current_window_handle(self):
        return self.driver.current_window_handle

    def all_window_handles(self):
        return self.driver.window_handles

    def switch_to_single_window(self):
        all_handles = self.driver.window_handles
        for handle in all_handles:
            self.driver.switch_to_window(handle)

    def switch_window(self):
        now_handle = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle is not now_handle:
                self.driver.switch_to_window(handle)
        return self.driver.current_window_handle

    def get_current_url(self):
        return self.driver.current_url

    '''
    解析table类型元素，返回字典类型
    e.g.
    {row1:[col1,col2,...], row2:[col1,col2,...],...}
    '''
    def load_table(self, page_name, table_data, table_name):
        table_text = self.find_element(get_element(page_name, table_data))
        table_title = self.find_element(get_element(page_name, table_name))
        table_text_rows = table_text.find_elements_by_tag_name('tr')
        table_cols = table_text_rows[0].find_elements_by_tag_name('td')
        table_title_rows2 = table_title.find_elements_by_tag_name('tr')
        table_field = table_title_rows2[0].find_elements_by_tag_name('th')
        table_name_list = []
        table_data_list = []
        table_field_list = []
        table_data_dic = {}
        for m in range(len(table_field)):
            table_field_list.append(table_title_rows2[0].find_elements_by_tag_name('th')[m].text)
        for i in range(len(table_cols)):
            for j in range(len(table_text_rows)):
                table_name_list.append(table_text_rows[j].find_elements_by_tag_name('td')[i].text)
                if j == len(table_text_rows) - 1:
                    table_data_list.append(table_name_list)
                    table_name_list = []
        for x in range(len(table_field_list)):
            table_data_dic[table_field_list[x]] = table_data_list[x]
        return table_data_dic

    '''
    支持JavaScript脚本运行，实现上传文件
    '''
    def execute_js_script(self, element_name, file_path):
        self.driver.execute_script("document.findElementByXpath(" + element_name + ").style.display='block';")
        self.driver.find_element_by_xpath(element_name).send_keys(file_path)

    '''
    登录
    '''
    def login(self,switch_button_loc="switch_button_loc"):
        page_handle = self.driver.current_window_handle
        ele =self.find_element(get_element("login_page", switch_button_loc))
        ele.click()

        #switch_window()
        now_handle = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle is not now_handle:
                self.driver.switch_to_window(handle)

        #send_keys(get_element("login_page", "username_text_loc"), "Yan123456")
        element1 = self.find_element(get_element("login_page", "username_input_loc"))
        element1.clear()
        element1.send_keys("Yan1234567")

        #验证码
        element2 = self.find_element(get_element("login_page", "password_input_loc"))
        element2.clear()
        element2.send_keys("Yan1234567")
        #图片验证码
        element3 = self.find_element(get_element("login_page", "verifyCode_input_loc"))
        element3.clear()
        element3.send_keys("8888")
        #确认登录
        ele1 = self.find_element(get_element("login_page", "login_button_loc"))
        ele1.click()

        time.sleep(2)
        self.driver.switch_to_window(page_handle)
        self.driver.refresh()

    def get_attribute(self,locator,attributes):
        element = self.driver.find_element(locator[0], locator[1])
        return  element.get_attribute(attributes)

    def get_cookies(self):
        return self.driver.get_cookies()

    def add_cookies(self,cookie_dic):
        self.driver.add_cookie(cookie_dic)
