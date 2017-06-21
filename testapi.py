# -*coding:utf-8*-
import requests

url = "https://api.douban.com/v2/book/user/ahbei/collections"
data = {"status": "read",
        "rating": 3,
        "tag": "小说"
        }