
a = "Hello World"

h = {
    "a": 1,
    "b": None,
    1: "hello",
    "d": (1,2),
    "f": [3,4],
    "f": {"1":"2"},
}

# 字典 增删改查

h["xx"] = "xxx" # 增
print(h)

del h["xx"]  # 删
print(h)

h["b"] = 2 # 改
print(h)

print(h["a"]) # 查询