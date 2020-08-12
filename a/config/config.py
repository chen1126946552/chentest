#!/usr/bin/env python3
# coding: utf-8
# 配置文件
import os
import sys

class Config(object):
    # 默认配置
    # 自动化数据入库的测试库连接信息
    MYSQL_HOST = "139.220.242.36"
    MYSQL_PORT = 23306
    MYSQL_USER = "qa_auto"
    MYSQL_PASSWD = "qa_auto"
    MYSQL_DB = "qa_auto_ptengine"

    # 获取接口列表文件的路径
    TABLE_PATH = os.path.dirname(os.path.realpath(__file__))

    # 生成报告的路径
    REPORT_DIR = "/data/www/qa/"

    def __getitem__(self, key):
        return self.__getattribute__(key)

class JPConfig(Config):
    # 日本生产环境
    AREA = 'jp'
    URL = 'https://reportv3.ptengine.jp'
    DC_URL = "https://hquery.ptengine.jp/d"
    EVENT_URL = "https://dmquery.ptengine.jp"
    COOKIE = "_ga=GA1.2.189976207.1561994306; _fbp=fb.1.1561994306207.1494341857; intercom-id-cfiqb37k=3f7b8fcb-b011-4f76-9946-952915085c0c; SREC_SESSION=V1.1561994310998; optimizelyEndUserId=oeu1561995219261r0.1588123560361232; optimizelyBuckets=%7B%7D; optimizelySegments=%7B%221453382414%22%3A%22gc%22%2C%221454342403%22%3A%22false%22%2C%221454532196%22%3A%22direct%22%2C%222758070244%22%3A%22false%22%2C%222779690603%22%3A%22direct%22%2C%222787750070%22%3A%22gc%22%7D; qtrans_front_language=en; _BEAMER_USER_ID_fTrebDrv14222=2ea73127-b2ec-4238-8c5a-89dfc946cdf1; utm_source=www.sorashido.com; utm_medium=Promo; utm_campaign=PTEngage; pt_699082d1=uid=&nid=0&vid=&vn=0&pvn=167&sact=1564648824602&to_flag=0&pl=qddrxWATMZd3/KL/CNA4KQ*pt*1564648824602; _jzqa=1.1720195963160708600.1563185414.1563855956.1564728702.7; _jzqx=1.1563185414.1564728702.1.jzqsr=reportv3%2Eptengine%2Ejp|jzqct=/.-; _qzja=1.661138201.1563185414316.1563855956227.1564728702232.1564729449092.1564729618397.0.0.0.21.7; _BEAMER_DATE_fTrebDrv14222=2019-08-12T02:23:39.959Z; intercom-session-f6gex48r=N1ZZRkhueXUwWkFPRTB2WjJpYm9PNDIxcVlhR3ZMWG1VOTFCMW9wYUpEdFpGOGdvZEJiKzRGemZLeHlZaFNVcC0tU3ArSnh4UzR6ckdWdlpla3ZJWTVoZz09--9bd314438f406602cd44c270788f36eaa447fbd9; currentSiteId=ad3e0082c6009491a34879410fb6d992a735b6c2f742816d9870979762a2b6a7; currentSiteId.sig=KEhVTBkuAR-q0lVtyOj_TywGdko; _BEAMER_LAST_POST_SHOWN_fTrebDrv14222=158105; _gid=GA1.2.350775595.1566185457; rememberkey=65de4653cbbb865b1b0ed50f682109d7312c565a6ba6a6ed68749c5367b0276a1c8c3382993f62d0be71e8ede80ce280f9a7730a9fff5a9c9b8e29c989eaf82ebea55bebc4b9be2d31db1badd537300f; rememberkey.sig=DldV36bR47b4M7qF_zUz8A9UPKo; pt_uid=1559198603558763; _8bfd0=http://10.42.13.105:3100; PTJPSESSIONID=nG7flndGlgbJZ_6_sREDBdxFxppyahup; PTJPSESSIONID.sig=Ql49qosznAPw9yJ4pY6qrayYsyY; _BEAMER_FILTER_BY_URL_fTrebDrv14222=false; intercom-session-cfiqb37k=ZEFnR1REdVlsaW5lMEZVQjJjSjJYQVJnMXJKU1BkVDRiSXdOUWE4ZEN5OE5lRVptUlJ4c3BhTFl1VDRwOUM1QS0tZ2hqbExaeFkzNHRuZklFVGpUblR3Zz09--2760d43be90199b3f4265ff74ef1c2a99685723c; _BEAMER_LAST_UPDATE_fTrebDrv14222=1566290255269; _gat_UA-112701314-1=1; _gat_UA-112706662-1=1; pt_566d12f9=uid=Hne69T6ol-4hXdONoKI5RA&nid=0&vid=3ecLBwyunRH6usWSz9HGpw&vn=437&pvn=1&sact=1566291378882&to_flag=0&pl=0p5ylU67YHYU-Cl7ZYhjmw*pt*1566291378882; pt_s_566d12f9=vt=1566291378882&cad="

    UID = '1559198603558763'
    SID = '678c8654'
    ENGAGE_ID1 = '1562324147080576'
    ENGAGE_ID2 = '1562658106203944'
    ENGAGE_ID3 = '1562658873600497'
    INTER_TABLE = "pt_inter_elapsed_time"
    # es 地址
    ES_RUL = 'http://eshbak.ptengine.com:19200'
    INTER_TABLE = "pt_inter_elapsed_time"
    ENGAGE_IDS = 'bbe28499-91d0-45f7-8aab-bb41623a7f0e'
    ENGAGE_TABLE = "pt_engage"
    # engage js地址
    ENGAGE_JS_URL = 'http://pteengagejs.ptengine.jp/engage.v2.js'
    # HB检查engage页面
    HB_ENGAGE_URL = 'http://datatest16.ptmind.com/jponline/alluser.html'
    CHROME_DRIVER = "/usr/chromedriver"

class CNConfig(Config):
    # 中国生产环境
    AREA = 'cn'
    URL = 'https://report.ptengine.cn'
    DC_URL = "https://hquery.ptengine.cn/d"
    EVENT_URL = "https://dmquery.ptengine.cn"
    COOKIE = "_ga=GA1.2.1087912101.1577073400; _fbp=fb.1.1577073400822.386267394; intercom-id-cfiqb37k=f077f600-e55e-49dc-ac27-03a469b6b2d6; _BEAMER_USER_ID_CbxqXZWX14308=e4915ebd-b80f-410d-9957-c05b265ae813; _BEAMER_FIRST_VISIT_CbxqXZWX14308=2019-12-23T03:56:43.679Z; hubspotutk=e67aef807384d8e9a1c4d11620cc44a6; pt_ref_613dedb9=https://help.ptengine.cn/; Hm_lvt_636610bfb0bdd2654aa990328237292a=1576139518,1577080671; _BEAMER_DATE_CbxqXZWX14308=2020-01-14T09:55:23.382Z; _fd85e=http://10.42.65.192:3200; beginHASH=; _gid=GA1.2.1496319894.1584498457; _8731e=http://10.42.54.190:80; _BEAMER_FILTER_BY_URL_CbxqXZWX14308=false; __hstc=34511038.e67aef807384d8e9a1c4d11620cc44a6.1577073407400.1583746997334.1584498473116.34; __hssrc=1; PTZHSESSIONID=v_KbHQMTqoMifCd4jWilqdPPgmMPYMfO; PTZHSESSIONID.sig=WxiHqR9zUGWmk7rnzZNqTNTYS3I; rememberkey=65de4653cbbb865b1b0ed50f682109d7312c565a6ba6a6ed68749c5367b0276a1c8c3382993f62d0be71e8ede80ce2801c2f657f36ac8b7a3d81f16702c58f36566921627967567c4731e85091a25722; rememberkey.sig=Sl3KZvTqY3B3rjHrruIJ45XJluc; pt_uid=1561471388658091; pt_z=100; _gat_UA-112701314-1=1; _gat_UA-112706662-1=1; intercom-session-cfiqb37k=RWw2aHBGQTJ1VzZoVG1JYXltcnBNSlFBNEx3T3hZbi9neWQ0bWJMb3pXNnNGUHA2ZGgzVVA5UVlkVFo4cDEzRS0tSThMK01TUGZCMlRkUG41WWpRc3ZXUT09--124d844f624949c5d65c3622090a0aa9bcdf2d1a; pt_s_613dedb9=vt=1584498665738&cad=; pt_engage_helper=1; pt_613dedb9=uid=oMfYI5JsVFeHoIk0xsuciw&nid=0&vid=YsUucgWlMhPR2al9i4n2Sw&vn=115&pvn=4&sact=1584498666382&to_flag=0&pl=Zc4NQfvV5P1XXR4riy/6jQ*pt*1584498666382; __hssc=34511038.5.1584498473116"
    UID = '1561471388658091'
    SID = '1a392c1b'
    ENGAGE_ID1 = '1561471473829903'
    ENGAGE_ID2 = '1563941700747539'
    ENGAGE_ID3 = '1563941991603682'
    INTER_TABLE = "pt_inter_elapsed_time_cn"

    ES_RUL = 'http://wqeshbak.ptmind.com:9500'
    INTER_TABLE = "pt_inter_elapsed_time_cn"
    ENGAGE_IDS = '18b510f0-cb4a-470b-8651-071766a40be4'
    ENGAGE_TABLE = "pt_engage_cn"
    ENGAGE_JS_URL = 'http://pteengagejs.ptengine.cn/engage.js'
    # HB检查engage页面
    HB_ENGAGE_URL = 'http://datatest16.ptmind.com/cnonline/alluser.html'
    CHROME_DRIVER = "/usr/chromedriver"

class DevConfig(CNConfig):
    # 开发环境
    REPORT_DIR = "/Users/ptmind/Desktop/auto/"
    INTER_TABLE = "pt_inter_elapsed_time_copy"
    ENGAGE_TABLE = "pt_engage_copy"
    # chromeDriver路径
    CHROME_DRIVER = "/Users/ptmind/Desktop/pt-gitlab/chromedriver"


# 环境映射关系
mapping = {
    'JP': JPConfig,
    'CN': CNConfig,
    'dev': DevConfig
}

try:
    env = sys.argv[3]
except:
    env = 'JP'
print(env)

APP_ENV = os.environ.get('APP_ENV', env)
# 实例化对应的环境
conf = mapping[APP_ENV]()