
from lxml import etree

htmldemo = '''  
<meta charset="UTF-8"> <!-- for HTML5 --> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<html><head><title>yoyo ketang</title></head>
 <body> 
<b><!--Hey, this in comment!--></b> 
<p class="title"><b>yoyoketang</b></p> 
<p class="yoyo" id="xxx" >这里是我的微信公众号：yoyoketang <br> 
<a href="http://www.cnblogs.com/yoyoketang/tag/fiddler/" class="sister" id="link1">fiddler教程</a><br> 
<a href="http://www.cnblogs.com/yoyoketang/tag/python/" class="sister" id="link2">python笔记</a><br> 
<a href="http://www.cnblogs.com/yoyoketang/tag/selenium/" class="sister" id="link3">selenium文档</a><br> 
快来关注吧！</p> 
<p class="story">...</p>
 '''
# etree HTML 解析html内容
demo = etree.HTML(htmldemo)

# 打印html 内容
t = etree.tostring(demo, encoding="utf-8",pretty_print=True)
# print(t)
# print(t.decode("utf-8"))

# xpath 定位元素

x = '//*[@id="link1"]'
nodes = demo.xpath('//*[@id="link1"]') # list
print(nodes[0])
print(nodes[0].text)

print(nodes[0].get("id"))
print(nodes[0].get("class"))
print(nodes[0].get("href"))

n = demo.xpath('//*[@id="xxx"]') # 父元素

a = n[0].xpath('//a') # 子元素
print(a[0].text)


