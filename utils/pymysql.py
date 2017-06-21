import pymysql.cursors
def selectBySql(sqls):
    connect = pymysql.Connect(
        host='10.82.12.76',
        port=3306,
        user='root',
        passwd='dbfin@123',
        db='cenpur',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    # 查询数据
    try:
        # 执行SQL语句
        cursor.execute(sqls)
        connect.commit()
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in results:
            return i
    except:
        print("Error: unable to fetch data")

    # 关闭连接
    cursor.close()
    connect.close()