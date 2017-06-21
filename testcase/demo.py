from utils.connectSQL import *

sql = "select state from cenpur_mall_goods where shop_id=2 and name='OnlyTest'"
print(connect_sql(sql))
