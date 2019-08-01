# -*- coding: UTF-8 -*-

import configtest1
import sys



print(sys.argv[1])
config = sys.argv[1]

if config == 'Config_1':
    a = configtest1.Config_1
else:
    a = configtest1.Config_2

print(a.ABTEST)