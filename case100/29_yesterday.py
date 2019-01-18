# -*- coding: UTF-8 -*-

#计算天数


# 引入 datetime 模块
import datetime
def getYesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday
 
# 输出
print(getYesterday())