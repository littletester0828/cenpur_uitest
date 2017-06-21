# -*- coding:utf-8 -*-
import yaml
import os

# file_name = os.path.dirname(os.getcwd()) + "\\config\\config.yaml"
file_name = "D:\\3、Work\\bdfintAutoTest\\config\\config.yaml"

# 读取元素定位文件路径
def get_file_path(page_name):
    # file_path = os.path.dirname(os.getcwd()) + "\\config\\%s"%page_name + ".yaml"
    file_path = "D:\\3、Work\\bdfintAutoTest" + "\\config\\%s"%page_name + ".yaml"
    return file_path


# 读取元素定位信息
def get_element(page_name, element_name):
    fr = open(get_file_path(page_name), 'r')
    data = yaml.load(fr)
    get_dic = data["element"][page_name][element_name]
    for key in get_dic:
        get_loc = (key, get_dic[key])
    fr.close()
    return get_loc


# 读取发件人邮箱地址
def sender_username():
    fr = open(file_name, 'r')
    data = yaml.load(fr)
    get_user = data["mail"]["sender"]["username"]
    fr.close()
    return get_user


# 读取发件人邮箱密码
def sender_psw():
    fr = open(file_name, 'r')
    data = yaml.load(fr)
    get_psw = data["mail"]["sender"]["password"]
    fr.close()
    return get_psw


# 读取收件人邮箱地址
def receiver_username():
    fr = open(file_name, 'r')
    data = yaml.load(fr)
    get_user = data["mail"]["receiver"]["username"]
    fr.close()
    return get_user


# 读取测试数据
def get_test_data(page_name):
    fr = open(get_file_path(page_name), 'r')
    data = yaml.load(fr)
    get_data = data["testdata"][page_name]
    fr.close()
    return get_data


def get_url(page_name):
    fr = open(file_name, 'r')
    data = yaml.load(fr)
    get_test_url = data["url"][page_name]
    fr.close()
    return get_test_url

