# 时间戳js2py.eval_js('timestamp = (new Date).getTime()')
import js2py
import requests
import json

js = js2py.EvalJs()
with open('F:\工作项目\饿了么\饿了么sign参数.js', 'r', encoding='utf-8') as r:
    js.execute(r.read())
tk = 'f06a6f2b327178ef13826c03a4ef88a0'
t = '1597212777862'
appkey = '12574478'
data = '{"channel":"health","searchType":1,"sortBy":"INTELLIGENCE","pn":1,"rn":10,"fromPage":"channel","brandFolding":true,"userId":0,"fromalipay":0,"terminal":999,"tag":1,"windowType":"3","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":22.5181696,"lng":113.917952,"latitude":22.5181696,"longitude":113.917952,"cityId":11,"bizChannel":"mobile.antispider.default"}'
res = js.getSign(tk, t, appkey, data)
print(res)
url = 'https://shopping.ele.me/h5/mtop.hasee.channellistservice.getchannellist/1.0/?jsv=3.0.0&appKey=12574478&t='+str(t)+'&sign='+res+'&type=originaljson&valueType=original&isUseH5Request=true&api=mtop.hasee.ChannelListService.getChannelList&v=1.0&windVaneOptions=%5Bobject%20Object%5D&ttid=h5%40android_chrome_84.0.4147.125&data={"channel":"health","searchType":1,"sortBy":"INTELLIGENCE","pn":1,"rn":10,"fromPage":"channel","brandFolding":true,"userId":0,"fromalipay":0,"terminal":999,"tag":1,"windowType":"3","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":22.5181696,"lng":113.917952,"latitude":22.5181696,"longitude":113.917952,"cityId":11,"bizChannel":"mobile.antispider.default"}'
headers = {
    'cookie':'cna=zIsAF+OMsUICAd9o/mdmySxs; UM_distinctid=1739e9386c6234-029f5a3bfae845-b7a1334-100200-1739e9386c74d1; ubt_ssid=fyrpuhmnxaw10yt40sq9pq1pws038rke_2020-07-30; ut_ubt_ssid=8bu84th7w8c2eo4l2m2e9cgjxn1znigx_2020-07-30; _utrace=45c29aa7585f4244a1e31f2910491180_2020-07-30; track_id=1596166389|c61a4407a51c10f46971be50d4a1201994f05d0bd8ce102c83|c1c90a99d43cdf98f8d04f43ab22a393; tzyy=2b9fb9a1cc65124204de5a5b6009b4c8; USERID=1337276074; UTUSER=1337276074; SID=CgAAAABPtTaq-gAEAADUU8eN-JD-qdxq76yINemvXHmrH27DxBgl4kcc; ZDS=1.0|1596792661|g6ezodhvu+KfrBwCbuaD2GRD6I0vPoypctKeqzvk6sZJr6RAx2RAIGSZMRchZwfoxpJRoEb3wdz99tSZwFHBjA==; t=7e9350427d383a90c931c49d90517ea3; t_eleuc4=id4=0%40BA%2FvuHCrrRj3aoscK7vMf5SYaOvXhCF3CZneEQ%3D%3D; unb=2205056384466; tfstk=cGmhBeZFQ2zQVwzilHZIUNcFx0YOZs6UOrUZbDI4VXNm5coNiAbNuCKRO5ln2a1..; l=Ag0NW28XG2O2syNMFEdm5voGnSKH1kG8; _m_h5_tk=f06a6f2b327178ef13826c03a4ef88a0_1597217990731; _m_h5_tk_enc=07382db1ddb2cec4e2ec3aadb6fac8d4; nr_security_map_key=67cb9e8a-5492-40bd-839a-27398227ba21; isg=BMDAvwLgi7B-dHelVgFaI6X3kU6SSaQTNRXpNzpRjFqktWDf4ll0o5bUyxt1BVzr; _orbit_h5_utils_channel_=mobile.antispider.default.1597212777811',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36'
    }
response = requests.get(url, headers=headers)
cookie_jar = response.cookies
print(json.loads(response.text))
print(cookie_jar)