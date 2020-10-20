from eleme import get_local, get_cookie, get_sign, getCookie, get_id, get_city, get_proxy, update_status_code, \
    update_shopindex
import json
import requests
import pymysql
import time
import random
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


# 发送请求，到详细的商店信息
def send_request(sign, cookie, data, t):
    # 隧道域名:端口号
    tunnel = "tps123.kdlapi.com:15818"
    username = "t10274047989492"
    password = "1ucxvh7x"
    proxy = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    # proxy = get_proxy()
    cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
    url = 'https://shopping.ele.me/h5/mtop.venus.shopresourceservice.getshopresource/1.0/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600652627979&_preview_hash=41973&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E17914057671267804770&entry_from=&id=2233307755&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23999_16464%232616%237139%23329_16464%233304%2310639%23336%22%7D&rankType=&rank_id=3b71d5e37cec44da9be53f52a5972098&refer=&spm=a2ogi.13893704.category-shopcard.d1&store_id=239793058&wid=2233307755'
    }
    params = {
        'jsv': '3.0.0', 'appKey': '12574478', 't': t, 'sign': sign, 'type': 'originaljson', 'valueType': 'original', 'isUseH5Request': 'true','api': 'mtop.venus.ShopResourceService.getShopResource','v': '1.0','windVaneOptions': '[object Object]','ttid': 'h5@pc_chrome_86.0.4240.75','data': data
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxy).text
    except:
        # update_status_code(proxy)
        # proxy = get_proxy()
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxy).text

    result = json.loads(response)
    # print(result)
    if result['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期']:
        # proxy = get_proxy()
        getCookie()
        cookie = get_cookie()
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
        sign_t = get_sign(data, cookie)
        sign = sign_t[0]
        t = sign_t[1]
        params = {
            'jsv': '3.0.0', 'appKey': '12574478','t': t,'sign': sign,'type': 'originaljson','valueType': 'original','isUseH5Request': 'true','api': 'mtop.venus.ShopResourceService.getShopResource','v': '1.0','windVaneOptions': '[object Object]','ttid': 'h5@pc_chrome_86.0.4240.75','data': data
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxy).text
        result = json.loads(response)
        return result
    elif result['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
        # update_status_code(proxy)
        while True:
            # proxy = get_proxy()
            try:
                response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxy).text
            except:
                # update_status_code(proxy)
                # proxy = get_proxy()
                response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxy).text
            res = json.loads(response)
            # print(res)
            if res['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
                # update_status_code(proxy)
                pass
            else:
                return res
    else:
        return result


def save_shopinfo(sign, cookie, data, t, city, shop_index):
    global catInfoList
    result = send_request(sign, cookie, data, t)
    if result == 0:
        pass
    else:

        shopinfo = result['data']['data']['shopInfo']
        storeId = shopinfo['storeId']
        shopName = shopinfo['name']
        monthSales = shopinfo['monthSales']
        shopScore = shopinfo['shopScore']
        address = shopinfo['address']

        # 活动和券
        shopActivityAndCoupons = result['data']['data']['shopActivityAndCoupons']
        shopActivity = shopActivityAndCoupons['shopActivity']['shopActivityList']  # 活动
        activity = ''
        for ac in shopActivity:
            activity += ac['msg']+';'
        shopCoupons = shopActivityAndCoupons['shopCoupons']['couponDetailList']  # 券
        coupons = ''
        for coupon in shopCoupons:
            amount = coupon['amount']
            infoDesc = coupon['infoDesc']
            m = amount+'元券'+infoDesc
            coupons += m+';'
        cats = ''
        cat1ids = ''
        error = 0
        try:
            catInfoList = result['data']['data']['shopCategoryInfo']['catInfoList']  # 品类
        except:
            error = 1
        if error == 0:
            for catinfo in catInfoList:
                if '❤' in catinfo['name'] or '🌟' in catinfo['name'] or '💏' in catinfo['name'] or '🤢' in catinfo['name'] or '🌡️' in catinfo['name'] or '💊' in catinfo['name'] or '👩‍💼' in catinfo['name']:
                    # print(catinfo['name']) # ☁,☯,✈,❤,🌟,💏,🤢,🌡️,💊, 👩‍💼,🔥
                    catinfo['name'].split('')

                    pass
                else:
                    cats += catinfo['name'] + ';'  # 品类名称
                cat1ids += str(catinfo['cat2Ids']) + ';'  # 品类ID
        else:
            cats = '无'
            cat1ids = '无'
        # print(cats)
        sql = 'insert into e_shop_info(storeId, shopName, monthSales, shopScore, address, activity, coupon, category, categoryIds, city)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (str(storeId), shopName, str(monthSales), str(shopScore), address, activity, coupons, str(cats), cat1ids, city))
            conn.commit()
        except:
            pass


def main_shopinfo():
    all_info = get_id()[0]
    lenth_all = len(all_info)  # 数据库所有的商店数据的长度
    shop_index = int(get_id()[1])  # 商店数据的下标
    for shop_index in range(shop_index, lenth_all):
        print('-----------------------------', shop_index)
        update_shopindex(shop_index)
        only_shop = all_info[shop_index]   # 获取下标为shop_index的商店
        storeId = only_shop[0]
        eleId = only_shop[1]
        wid = only_shop[2]
        lat = only_shop[3]
        lng = only_shop[4]
        cookie = get_cookie()
        city_info = get_city(lat, lng, cookie)
        city = city_info[0]
        city_id = city_info[1]
        data = '{"storeId":' + storeId + ',"wid":' + wid + ',"eleId":'+'"'+eleId+'"'+',"itemId":"","sceneSugItemIds":"","venusAnchorType":0,"isShowGuessLike":0,"isRankByAlg":0,"isCatRankByAlg":0,"cityId":'+str(city_id)+',"coordsOnly":1,"livingShowChannel":"others","deviceId":"583A444CAB6A47DEA021D46336ECA533|1601271713038","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"bizChannel":"mobile.default.default"}'
        sign_t = get_sign(data, cookie)
        sign = sign_t[0]
        t = sign_t[1]
        # time.sleep(random.randint(2, 6))
        save_shopinfo(sign, cookie, data, t, city, shop_index)


if __name__ == '__main__':
    main_shopinfo()

# 有不存在shopinfo的情况

