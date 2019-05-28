import os

# 获取当前执行的文件路径
filepath = os.path.realpath(__file__)
print(filepath)

# 获取文件夹路径
foderpath = os.path.dirname(filepath)
print(foderpath)

# 连接路径
a = os.path.join(foderpath,'case')
print(a)

# 判断文件路径是否存在
b = os.path.exists(os.path.join(foderpath,'case'))
print(b)

if not b:
    os.mkdir(os.path.join(foderpath,'case'))