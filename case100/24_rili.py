# -*- coding: UTF-8 -*-

#生成日历

import calendar

# 输入指定年月
yy = int(input("输入年份: "))
mm = int(input("输入月份: "))
 
# 显示日历
print(calendar.month(yy,mm))
