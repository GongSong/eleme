from eleme import get_local, get_cookie, get_sign, getCookie, get_timestamp, get_proxy, get_city, update_status_code
import json
import requests
import random
import pymysql
import time
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()
flag = 0


# 发送请求获取响应
def send_request(data, sign, cookie, t):
    proxy = get_proxy()
    cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
    url = 'https://shopping.ele.me/h5/mtop.hasee.channellistservice.getchannellist/1.0/'
    headers = {
        'referer': 'https://h5.ele.me/newretail/p/channel/?channel=health',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    }
    params = {
        'jsv': '3.0.0', 'appKey': '12574478', 't': t, 'sign': sign, 'type': 'originaljson', 'valueType': 'original','isUseH5Request': 'true', 'api': 'mtop.venus.ShopResourceService.getShopResource', 'v': '1.0','windVaneOptions': '[object Object]', 'ttid': 'h5@pc_chrome_86.0.4240.75', 'data': data
    }
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False, proxies=proxy)
    except:
        update_status_code(proxy)
        proxy = get_proxy()
        response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False, proxies=proxy)
    res = json.loads(response.text)
    print(res)
    if res['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期'] or res['ret'] == ['FAIL_SYS_TOKEN_ILLEGAL::非法令牌']:
        proxy = get_proxy()
        getCookie()
        cookie = get_cookie()
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
        sign_t = get_sign(data, cookie)
        sign = sign_t[0]
        t = sign_t[1]
        params = {
            'jsv': '3.0.0', 'appKey': '12574478', 't': t, 'sign': sign, 'type': 'originaljson', 'valueType': 'original','isUseH5Request': 'true','api': 'mtop.venus.ShopResourceService.getShopResource','v': '1.0','windVaneOptions': '[object Object]','ttid': 'h5@pc_chrome_86.0.4240.75','data': data
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False, proxies=proxy)
        res_one = json.loads(response.text)
        if res_one['data'] == {'errorCode': '0', 'errorDesc': '成功'}:
            return 0
        elif res_one['data'] == {}:
            pass
        else:
            return res_one
    elif res['data'] == {'errorCode': '0', 'errorDesc': '成功'}:
        return 0
    elif res['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
        while True:
            proxy = get_proxy()
            result = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False,proxies=proxy)
            res_two = json.loads(result.text)
            print(res_two)
            if res_two['data'] == {'errorCode': '0', 'errorDesc': '成功'}:
                pass
            elif res_two['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
                update_status_code(proxy)
                pass
            else:
                return res_two
    else:
        shop_list = res['data']['data']['shoplist']
        print('本页商店总数--------------------------------', len(shop_list))
        return shop_list


# 保存商店列表数据
def save_shoplist(data, sign, cookie, t, lat, lng):
    res = send_request(data, sign, cookie, t)
    if res == 0:
        pass
    else:
        shop_list = res['data']['data']['shoplist']
        print('本页商店总数--------------------------------', len(shop_list))
        for shop in shop_list:
            shopname = shop['name']
            eleId = shop['eleId']
            monthSales = shop['monthSales']
            wid = shop['wid']
            try:
                shopScore = shop['shopScore']
            except:
                shopScore = '无'
            storeId = shop['storeId']
            lat = lat
            lng = lng
            if '眼镜' in shopname or '成人' in shopname or '趣' in shopname or '优品' in shopname or '口腔' in shopname or '体检' in shopname or '色' in shopname:
                pass
            else:
                print(shopname, eleId, str(monthSales), wid, shopScore, storeId, type(lat), type(lng))
                try:
                    sql = 'insert into ele_shop(storeId, shopName, eleId, monthSales, shopScore, wid, lat, lng)values (%s,%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql, (
                    str(storeId), shopname, str(eleId), str(monthSales), shopScore, wid, str(lat), str(lng)))
                    conn.commit()
                except:
                    pass
        num = res['data']['data']['total']
        return num



def main():
    lngs = get_local()[0]
    lats = get_local()[1]
    flag = get_local()[2]
    for index in range(flag, len(lats)):
        cookie = get_cookie()
        lng = lngs[index]
        lat = lats[index]
        print(lng, lat, '---------------------定位', index)
        sql = 'update get_cookie set flag=%s' % ('"' + str(index) + '"')
        cursor.execute(sql)
        conn.commit()
        # time.sleep(random.randint(5, 10))
        city_info = get_city(lat, lng, cookie)
        print(city_info)
        try:
            id = city_info[1]
        except:
            id = 14
        for i in range(1, 6):
            data = '{"channel":"health","searchType":1,"sortBy":"INTELLIGENCE","pn":'+str(i)+',"rn":20,"fromPage":"channel","brandFolding":true,"userId":0,"fromalipay":0,"terminal":999,"tag":1,"windowType":"3","deviceId":"583A444CAB6A47DEA021D46336ECA533|1601271713038","lat":' + str(lat) + ',"lng":' + str(lng) + ',"latitude":' + str(lat) + ',"longitude":' + str(lng) + ',"cityId":'+str(id)+',"bizChannel":"mobile.default.default"}'
            sign_t = get_sign(data, cookie)
            sign = sign_t[0]
            t = sign_t[1]
            num = save_shoplist(data, sign, cookie, t, lat, lng)
            if num < 20 or num == 0:  # 如果请求返回的无数据就停止进行请求
                break


if __name__ == '__main__':
    main()

