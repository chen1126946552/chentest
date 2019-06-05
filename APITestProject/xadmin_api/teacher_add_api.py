import requests
import re
from requests_toolbelt import MultipartEncoder
from lxml import etree

def teacher_add(s):
    # 登录成功之后的请求
    url3 = "http://47.104.190.48:8000/xadmin/hello/teacher/add/"

    r_token = s.get(url3)
    token2 = re.findall('name="csrfmiddlewaretoken" value="(.+?)"', r_token.text)
    print("获取添加页面的token值")
    print(token2[0])

    body = MultipartEncoder(
        fields=[
            ("csrfmiddlewaretoken", token2[0]),
            ("csrfmiddlewaretoken", token2[0]),
            ("teacher_name", "test0002"),
            ("tel", "112211"),
            ("mail", "1111@qq.com"),
            ("_save", ""),
        ]
    )
    r3 = s.post(url3, data=body, headers={'Content-Type': body.content_type})

# 判断是否成功
# SQL查询也可以

def get_teacher_add_text(s):
    '''查询列表页面 第一个数据'''
    url4 = "http://47.104.190.48:8000/xadmin/hello/teacher/"
    r4 = s.get(url4)

    # xpath定位
    x = '//*[@id="changelist-form"]/div[1]/table/tbody/tr[1]/td[2]/a'
    demo = etree.HTML(r4.text)
    nodes = demo.xpath(x)
    print("获取列表页面的第一个数据：%s"%nodes[0].text)
    return nodes[0].text


# sql 查询数据库， name 数据条数   x
# 新增一组数据
# sql查询数据库，name 数据条数 y
# 断言  x+1 == y



