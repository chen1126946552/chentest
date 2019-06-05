
def test(x,y):
    return x+y

def xiangcheng(a,b):
    return a*b

if __name__ == "__main__":
    # 下面是测试调试的代码
    r = test(1,1) # 实际结果
    print(r)
    exp = 2 # 期望结果
    assert r == exp  #断言

    r1 = xiangcheng(2,3)
    exp = 6
    assert r1 == exp