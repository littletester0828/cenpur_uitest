# -*-coding:utf-8 -*-
import pymysql


def connect_sql(sql):
    db = pymysql.connect("10.82.12.76", "root", "dbfin@123", "cenpur")
    cursor = db.cursor()
    cursor.execute(sql)
    search_result = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return search_result
