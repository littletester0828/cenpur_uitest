import time
import unittest
from pyse.init_pyse import Pyse
from utils.loadyaml import *
from testlibs.log import Logger
from utils.pymysql import selectBySql
from utils.connectSQL import *
import re
#
autolog = Logger()
userId="9c9689311f034619b8d22640154e6ffc"
def getCode(codeLine):
    '''
    去掉商品编号
    输入：商品编号：PTSP20170613090924301输出：PTSP20170613090924301
    '''
    switchLine = str(codeLine)
    code = switchLine[-21:]
    return code
def getUnit(price_unit):
    '''
    把价格单位转化为重量单位
    输入 元/干吨  输出 干吨
    '''
    price_unit_text = str(price_unit)
    indexes1 = price_unit_text.find("/")+1
    unit = price_unit_text[indexes1:]
    return unit
def getNum(num):
    '''
        把价格精确两位小数转化为精确到个位
        输入 20.00  输出 20吨
        '''
    price_text = str(num)
    indexes1 = price_text.find(".")
    price = price_text[0:indexes1]
    return price
def getDicSql(cn_nameOFdic,ColumnOfgoods,code):
    '''通过dic表cn_name的value值和goods表的列名、商品编号来获取某个商品字段的显示字段'''
    result =selectBySql("SELECT label_value from cenpur_user_dict where en_name ='%s' and value=(select %s from cenpur_mall_goods where code ='%s')"%(cn_nameOFdic,ColumnOfgoods,code))
    return  result


class ProductDetail(unittest.TestCase):

    def setUp(self):
        self.driver = Pyse('chrome')
        self.driver.open(get_url("home_page"))
        # 登录点击第一个商品
        self.driver.login()
        self.driver.click(get_element("productDetail_page", "firstLineName"))
        time.sleep(1)
    '''
    setUP
    登录
    '''

    def test_1_MBXProductLink(self):
        '''面包屑导航链接-大宗交易'''
        self.driver.click(get_element("productDetail_page","MBXProductPage_link_loc"))
        time.sleep(1)
        url=self.driver.get_current_url()
        autolog.info(url)
        assert url=="http://10.82.12.25/centralize-purchase/#/product",("链接未跳转成功")
        autolog.info("导航链接大宗交易页面正确")
    '''
    test_1_MBXProductLink
    面包屑导航-大宗交易-链接
    点击后跳转大宗交易页面
    比对页面url
    '''
    def test_2_MBXHomeLink(self):
        '''面包屑导航链接-首页'''
        self.driver.click(get_element("productDetail_page","MBXHomePage_link_loc"))
        time.sleep(1)
        url = self.driver.get_current_url()
        autolog.info(url)
        assert url=="http://10.82.12.25/centralize-purchase/#/",("链接未跳转成功")
        autolog.info("导航链接首页正确")
    '''
    test_2_MBXHomeLink
    面包屑导航-首页-链接
    点击后跳转首页
    比对页面url
    '''

    def test_3_goodImg(self):
        '''商品图片展示'''
        src = self.driver.get_attribute(get_element("productDetail_page", "good_img_loc"), "src")
        if src:
            self.driver.open(str(src))
            assert self.driver.get_title() != "404 Not Found"
            autolog.info(src)
            autolog.info("商品图片展示正常")
        else:
            autolog.info("无法获取src")
            assert False, ("获取src失败")
        self.assertTrue(src, "无法获取src")
    '''
    test_3_goodImg
    商品图片的展示,看是否可以访问图片地址
    '''
    def test_4_mainGoodType(self):
        '''主要信息：商品类型：期货/现货'''
        eletext =self.driver.find_element(get_element("productDetail_page","goodCode_text_loc"))
        autolog.info("获取到：%s"%eletext.text)
        code=getCode(eletext.text)
        autolog.info(code)
        #通过商品编号查询出商品类型
        type = getDicSql("type","type",code)
        # type = selectBySql("SELECT label_value from cenpur_user_dict where en_name ='type' and value=(select type from cenpur_mall_goods where code ='%s')"%code)
        autolog.info(type)
        text = self.driver.text_in_element(get_element("productDetail_page","goodType_text_loc"),type[0])
        autolog.info(text)
        if text:
            autolog.info("商品类型显示正确")
            assert True
        else:
            autolog.info("商品类型显示错误")
            assert False,("商品类型显示错误")
    '''
    test_4_mainType
    主要信息的商品类型展示：现货/期货
    通过页面获取商品编号
    通过商品编号获取数据库中的商品类型显示信息
    比对商品类型是否显示
    '''
    def test_5_mainGoodPrice(self):
        '''主要信息-商品价格'''
        #获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        #查询数据库
        price_unit = getDicSql("price_unit","price_unit",code)
        price = selectBySql("SELECT price from cenpur_mall_goods where code ='%s'"%code)
        autolog.info(price)
        autolog.info(price_unit)
        #获取价格
        eletext1 = self.driver.find_element(get_element("productDetail_page","goodPrice_text_loc"))
        text =eletext1.text
        autolog.info(text)
        #判断
        re1 = text.find("￥")
        re2 = text.find(getNum(price[0]))
        re3 = text.find(str(price_unit[0]))
        re4 = str(price_unit[0]).find("美元")
        if re2!=-1 and re3!=-1:
            autolog.info("单位、价格验证正确")
            if re4==0 and re1==-1:
                autolog.info("单位美元$")
                assert True
            elif re4==-1 and re1==0:
                autolog.info("单位元￥")
                assert True
            else:
                autolog.info("单位￥/$显示错误")
                assert False,("单位￥/$显示错误")
        else:
            autolog.info("单位、价格错误")
            assert False,("单位、价格错误")
    '''
    test_5_mainGoodPrice
    主要信息中价格的显示
    通过页面获取商品编号
    通过商品编号获取数据库中的价格和单位
    通过判断价格、单位、单位符号是否正确
    '''
    def test_6_mainName(self):
        '''主要信息-商品名称'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        name = selectBySql("SELECT name from cenpur_mall_goods where code ='%s'"%code)
        autolog.info(name)
        #获取名称
        text = self.driver.text_in_element(get_element("productDetail_page","goodName_text_loc"),name[0])
        autolog.info(text)
        if text:
            autolog.info("商品名称显示正确")
            assert True
        else:
            autolog.info("商品名称显示正确")
            assert False,("商品名称显示正确")
    '''
    test_6_mainName
    主要信息：商品名
    获取商品编号
    查询数据库中商品名
    与页面商品名做对比
    '''
    def test_7_mainPriceType(self):
        '''主要信息-计价方式'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        goods_type = connect_sql("select type from cenpur_mall_goods where code = '%s'" % code)
        print('2')
        if goods_type[0][0] == 1:
            price_type = getDicSql("price_type", "price_type", code)
            autolog.info(price_type)
            # 获取计价方式
            text = self.driver.text_in_element(get_element("productDetail_page", "goodPriceType_text_loc"),
                                               price_type[0])
            autolog.info(text)
            if text:
                autolog.info("计价方式显示正确")
                assert True
            else:
                autolog.info("计价方式显示错误")
                assert False, ("计价方式显示错误")
        else:
            terms_price = getDicSql("terms_price", "terms_price", code)
            autolog.info(terms_price)
            # 获取价格术语
            text = self.driver.text_in_element(get_element("productDetail_page", "goodPriceType_text_loc"),
                                               terms_price[0])
            autolog.info(text)
            if text:
                autolog.info("价格术语显示正确")
                assert True
            else:
                autolog.info("价格术语显示错误")
                assert False, ("价格术语显示错误")

    '''
    test_7_priceType
    主要信息：计价方式
    获取商品编号
    查询数据库中计价方式信息
    与页面获取的计价方式作对比
    '''
    def test_8_mainTagoutNum(self):
        '''主要信息-发盘量'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        price_unit = getDicSql("price_unit", "price_unit", code)
        tagout_num = selectBySql("SELECT tagout_num from cenpur_mall_goods where code ='%s'" % code)
        unit=getUnit(price_unit[0])
        autolog.info(tagout_num)
        autolog.info(price_unit)
        autolog.info(unit)
        # 获取发盘量
        eletext1 = self.driver.find_element(get_element("productDetail_page", "goodTagoutNum_text_loc"))
        text = eletext1.text
        autolog.info(text)
        # 判断
        re1 = text.find(getNum(tagout_num[0]))
        re2 = text.find(str(unit))
        if re1 != -1 and re2 != -1:
            autolog.info("单位、发盘量验证正确")
        else:
            autolog.info("单位、发盘量错误")
            assert False, ("单位、发盘量错误")
    '''
    test_8_mainTagoutNum
    获取商品编号
    查询数据库中发盘量、单位信息
    与页面获取的发盘量作对比
    '''
    def test_9_1_mainStartNum(self):
        '''主要信息-起订量'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        price_unit = getDicSql("price_unit", "price_unit", code)
        start_num = selectBySql("SELECT start_num from cenpur_mall_goods where code ='%s'" % code)
        unit = getUnit(price_unit[0])
        autolog.info(start_num)
        autolog.info(price_unit)
        autolog.info(unit)
        # 获取起订量
        eletext1 = self.driver.find_element(get_element("productDetail_page", "goodStartNum_text_loc"))
        text = eletext1.text
        autolog.info(text)
        # 判断
        re1 = text.find(getNum(start_num[0]))
        re2 = text.find(str(unit))
        if re1 != -1 and re2 != -1:
            autolog.info("单位、起订量验证正确")
        else:
            autolog.info("单位、起订量错误")
            assert False, ("单位、起订量错误")
    '''
    test_9_mainStartNum
    获取商品编号
    查询数据库中起订量、单位信息
    与页面获取的起订量作对比
    '''
    def test_9_2_mainsurrplus(self):
        '''主要信息：剩余量'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        price_unit = getDicSql("price_unit", "price_unit", code)
        surrplus = selectBySql("SELECT surplus from cenpur_mall_goods where code ='%s'" % code)
        unit = getUnit(price_unit[0])
        autolog.info(surrplus)
        autolog.info(price_unit)
        autolog.info(unit)
        # 获取剩余量
        eletext1 = self.driver.find_element(get_element("productDetail_page", "goodSurplusNum_text_loc"))
        text = eletext1.text
        autolog.info(text)
        # 判断
        re1 = text.find(getNum(surrplus[0]))
        re2 = text.find(str(unit))
        if re1 != -1 and re2 != -1:
            autolog.info("单位、剩余量验证正确")
        else:
            autolog.info("单位、剩余量错误")
            assert False, ("单位、剩余量错误")
    '''
    test_10_mainsurrplus
    获取商品编号
    查询数据库中剩余量、单位信息
    与页面获取的剩余量作对比
    '''
    def test_9_3_mainNumText(self):
        '''采购量输入框'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        # 查询数据库
        start_num = selectBySql("SELECT start_num from cenpur_mall_goods where code ='%s'" % code)
        surplus = selectBySql("SELECT surplus from cenpur_mall_goods where code ='%s'" % code)
        autolog.info(start_num)
        autolog.info(surplus)
        #操作
        #小于起订量
        self.driver.send_keys(get_element("productDetail_page","goodNum_textBox_loc"),str(int(getNum(start_num[0]))-1))
        self.driver.click(get_element("productDetail_page","goodType_text_loc"))#点击失去焦点
        eleStart =self.driver.find_element(get_element("productDetail_page","goodNum_textBox_loc"))
        eleStart_num=int(eleStart.get_attribute("value"))
        #大于剩余量
        self.driver.send_keys(get_element("productDetail_page", "goodNum_textBox_loc"), str(int(getNum(surplus[0]))+1))
        self.driver.click(get_element("productDetail_page", "goodType_text_loc"))  # 点击失去焦点
        eleSurplus = self.driver.find_element(get_element("productDetail_page", "goodNum_textBox_loc"))
        eleSurplus_num = int(eleSurplus.get_attribute("value"))

        assert eleStart_num>=int(start_num[0]) and eleSurplus_num<=int(surplus[0]),("小于起订量或者大于剩余量")
        autolog.info("输入框验证正确")
    '''
    test_11_mainBuyDown
    通过商品编号，查询数据库中的起订量和剩余量
    输入小于起订量和大于剩余量的数字
    '''
    def test_9_4_mainCollection(self):
        '''收藏商品'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        #删除我的收藏
        selectBySql("delete  from cenpur_mall_favorites where user_id ='%s'"%userId)
        #获取class
        class1 = self.driver.get_attribute(get_element("productDetail_page","goodCollection_button_loc"),"class")
        self.driver.click(get_element("productDetail_page","goodCollection_button_loc"))
        class2 =self.driver.get_attribute(get_element("productDetail_page","goodCollection_button_loc"),"class")
        #去我的收藏页验证
        self.driver.open(get_url("favorite_page"))
        self.driver.refresh()
        eletext1 = self.driver.find_element(get_element("productDetail_page","favoriteCode_text_loc"))
        autolog.info("我的收藏页%s"%eletext1.text)
        code1 = getCode(eletext1.text)
        autolog.info(code1)

        assert class1==class2 and code==code1,("商品未成功收藏")
        autolog.info("商品成功收藏")

    '''
    test_12_mainCollection
    点击收藏后，验证收藏标签的class是否变化
    然后进入我的收藏页面，找到商品编号，看是否相同
    '''

    def test_9_5_shopImg(self):
        '''店铺图片'''
        src = self.driver.get_attribute(get_element("productDetail_page", "shop_img_loc"), "src")
        if src:
            self.driver.open(str(src))
            assert self.driver.get_title() != "404 Not Found"
            autolog.info(src)
            autolog.info("店铺页面图片展示正常")
        else:
            autolog.info("无法获取src")
            assert False, ("获取src失败")

    '''
    test_13_shopImg
    商品图片的展示,看是否可以访问图片地址
    '''
    def test_9_6_shopPhone(self):
        '''店铺-电话展示'''
        # 获取商品编号
        eletext = self.driver.find_element(get_element("productDetail_page", "goodCode_text_loc"))
        autolog.info("获取到：%s" % eletext.text)
        code = getCode(eletext.text)
        autolog.info(code)
        #获取联系方式
        phone = selectBySql("select phone from cenpur_mall_shop where id=(SELECT shop_id from cenpur_mall_goods where code='%s')"%code)
        autolog.info(phone)
        #获取页面信息判断
        text = self.driver.text_in_element(get_element("productDetail_page","shopPhone_text_loc"),str(phone[0]))
        if text:
            autolog.info("店铺电话号码正确")
            assert True
        else:
            autolog.info("店铺电话号码错误")
            assert False,("店铺电话号码错误")
    '''
    test_14_shopPhone
    店铺号码展示
    通过商品编号，查询对应的店铺信息
    通过获取联系方式
    与页面做对比
    '''
    def test_9_7_GOshop(self):
        '''进入店铺'''
        self.driver.click(get_element("productDetail_page","goShop_button_loc"))
        time.sleep(2)
        url = self.driver.get_current_url()
        autolog.info("点击进入店铺后跳转页面为：%s" % url)
        self.assertIn("storeDetail", url, "未成功跳转店铺详情页面")
    '''
    test_15_GOshop
    进入店铺详情，对比url
    '''
    def test_9_8_shopCollection(self):
        '''收藏店铺'''
        # 删除我的收藏
        selectBySql("delete  from cenpur_mall_favorites where user_id ='%s'" % userId)
        autolog.info("收藏店铺已删除")
        #收藏后进入我的收藏
        self.driver.click(get_element("productDetail_page","shopCollection_button_loc"))
        autolog.info("点击收藏店铺")
        self.driver.open(get_url("favorite_page"))
        time.sleep(2)
        self.driver.click(get_element("productDetail_page","faveritePageShop_link_loc"))
        time.sleep(1)
        ele_displayed = self.driver.find_element(get_element("productDetail_page","favoritePageShopName_text_loc")).is_displayed()
        autolog.info(ele_displayed)
        assert ele_displayed==True,("收藏的店铺元素不存在")
        autolog.info("店铺收藏成功")
    '''
    test_16_shopCollection
    清空我的收藏
    点击收藏店铺
    进入我的收藏页面查找是否有收藏的店铺
    '''
    def tearDown(self):
        self.driver.close()
        autolog.info("tearDown")

if __name__ == '__main__':
    unittest.main()
