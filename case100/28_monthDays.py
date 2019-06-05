# -*- coding: UTF-8 -*-

#计算天数

import calendar

year = int(input('请输入年份: '))
month = int(input('请输入月份: '))

monthRange = calendar.monthrange(year,month)

print(monthRange[1])