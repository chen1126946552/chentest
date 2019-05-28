import requests

url = "http://47.104.190.48:8000/weather_json"

par = {
    "time": "2019-04-10",
    "city": "北京"
}

r = requests.get(url, params=par)

print(r.text) # 确认返回是不是json

reason = r.json()['reason']
print(reason)

detail = r.json()['detail']
print(detail)

print(detail[0]['weather_name'])

for i in detail:
    if i['data'] == '2019-04-05':
        print(i)
        print(i['weather_name'])