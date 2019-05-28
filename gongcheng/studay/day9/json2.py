import json

h = {
    "a": 1,
    "b": None,
    1: "hello",
    "d": (1,2),
    "f": [3,4],
    "g": {"1":"2"},
    "h": True
}

 # dict 转json

dict_json = json.dumps(h, indent=4)
print(dict_json)

# json 转 dict
json_dict = json.loads(dict_json)
print(json_dict)