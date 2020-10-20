from eleme import get_local, get_cookie, get_sign, getCookie, get_city
import json
import requests
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


def send_request(sign, cookie, data, t):
    tunnel = "tps123.kdlapi.com:15818"
    username = "t10274047989492"
    password = "1ucxvh7x"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
    url = 'https://shopping.ele.me/h5/mtop.venus.shopcategoryservice.getcategorydetail/1.1/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600746916808&_preview_hash=16767&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E5997160818204947240&entry_from=&id=2233308144&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23724_16464%232616%237139%23349_16464%233304%2310639%23864%22%7D&rankType=&rank_id=cde52d4637bd420fa280fc1a08dc513c&refer=&spm=a2ogi.13893704.category-shopcard.d5&store_id=239785129&wid=2233308144',
    }
    params = {
        'jsv': '3.0.0', 'appKey': '12574478', 't': t, 'sign': sign, 'type': 'originaljson', 'valueType': 'original','isUseH5Request': 'true', 'api': 'mtop.venus.ShopResourceService.getShopResource', 'v': '1.0','windVaneOptions': '[object Object]', 'ttid': 'h5@pc_chrome_86.0.4240.75', 'data': data
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies).text
    except:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies).text
    result = json.loads(response)
    print(result)
    if result['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期']:
        getCookie()
        cookie = get_cookie()
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600746916808&_preview_hash=16767&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E5997160818204947240&entry_from=&id=2233308144&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23724_16464%232616%237139%23349_16464%233304%2310639%23864%22%7D&rankType=&rank_id=cde52d4637bd420fa280fc1a08dc513c&refer=&spm=a2ogi.13893704.category-shopcard.d5&store_id=239785129&wid=2233308144',
        }
        sign_t = get_sign(data, cookie)
        sign = sign_t[0]
        t = sign_t[1]
        params = {
            'jsv': '3.0.0', 'appKey': '12574478', 't': t, 'sign': sign, 'type': 'originaljson', 'valueType': 'original','isUseH5Request': 'true', 'api': 'mtop.venus.ShopResourceService.getShopResource', 'v': '1.0','windVaneOptions': '[object Object]', 'ttid': 'h5@pc_chrome_86.0.4240.75', 'data': data
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies).text
        result = json.loads(response)
        return result
    elif result['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
        for i in range(4):
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies).text
            res = json.loads(response)
            print(res)
            if res['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
                pass
            elif res['data'] == {'data': '110002 - 参数错误', 'errorCode': '110002', 'errorDesc': '参数错误'}:
                pass
            else:
                for drug_data in res['data']['data']:
                    print(len(drug_data['foods']), '------------药品数量')
                    for food in drug_data['foods']:
                        save_drug(food)
                    rankId = drug_data['rankId']
                    if len(drug_data['foods']) > 20:
                        return rankId
                    else:
                        return 0
    else:
        for drug_data in result['data']['data']:
            print(len(drug_data['foods']), '------------药品数量')
            for food in drug_data['foods']:
                save_drug(food)
            rankId = drug_data['rankId']
            if len(drug_data['foods']) > 20:
                return rankId
            else:
                return 0



# 存储药品数据
def save_drug(food):
    storeId = food['storeId']
    drug_name = food['name']
    eleSkuId = food['eleSkuId']
    upc = food['upc']
    monthSell = food['monthSell']
    currentPrice = food['currentPrice']
    originalPrice = food['originalPrice']
    if originalPrice == '':
        originalPrice = '无'
    categoryIds = food['categoryIds']
    print(storeId, drug_name, eleSkuId, upc, monthSell, currentPrice, originalPrice, categoryIds[0])
    try:
        sql = 'insert into ele_drug_info(storeId, drug_name, eleSkuId, upc, monthSell, currentPrice, originalPrice, categoryIds)values (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (storeId, drug_name, eleSkuId, upc, monthSell, currentPrice, originalPrice, categoryIds))
        conn.commit()
    except:
        pass


# 更新storeId的下标
def update_storeId_index(x):
    sql = 'update get_cookie set storeId_index=' + '"' + str(x) + '"'
    cursor.execute(sql)
    conn.commit()


# 获取数据库storeId的下标
def get_storeId_index():
    sql = 'select storeId_index from get_cookie'
    cursor.execute(sql)
    storeId_index = cursor.fetchone()[0]
    conn.commit()
    return storeId_index


# 数据库获取爬取药品所需要的药店信息
def get_shopinfo (storeId):
    sql = 'select categoryIds from e_shop_info where storeId=' + '"' + storeId + '"'
    cursor.execute(sql)
    categoryIds = cursor.fetchone()[0]  # 获取e_shop_info中的storeId和categoryIds
    conn.commit()
    sql1 = 'select lat, lng from ele_shop where storeId=' + '"' + storeId + '"'
    cursor.execute(sql1)
    lat_lng = cursor.fetchone()
    conn.commit()
    return categoryIds, lat_lng


# 获取药店的storeId
def get_storeId():
    sql = 'select storeId from e_shop_info'
    cursor.execute(sql)
    storeIds = cursor.fetchall()
    return storeIds


# 获取药品信息的主函数
def main_druginfo():
    storeIds = get_storeId()
    storeId_index = int(get_storeId_index())
    for x in range(storeId_index, len(storeIds)):
        print('第'+str(storeId_index)+'个药店')
        storeId = storeIds[x][0]
        update_storeId_index(x)
        shopinfo = get_shopinfo(storeId)
        lat_lng = shopinfo[1]
        lat = lat_lng[0]
        lng = lat_lng[1]
        if shopinfo[0] == '无':
            pass
        cat2Ids = (shopinfo[0]).split(';')
        for cat2Id in cat2Ids:
            cat3Ids = cat2Id.split(',')
            for i in range(len(cat3Ids)):
                cat3Id = cat3Ids[i]
                while True:   # 翻页需要参数rankId
                    cookie = get_cookie()
                    city_info = get_city(lat, lng, cookie)
                    city = city_info[0]
                    city_id = city_info[1]
                    data = '{"storeId":' + '"' + storeId + '"' + ',"categoryIds":"[' + cat3Id + ']","type":1,"pn":1,"rn":20,"sortBy":"","isShowGuessLike":"0","isRankByAlg":"0","version":"1.1","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"cityId":'+str(city_id)+',"bizChannel":"mobile.antispider.default"}'
                    sign_t = get_sign(data, cookie)
                    sign = sign_t[0]
                    t = sign_t[1]
                    rankId = send_request(sign, cookie, data, t)
                    if rankId == 0:
                        break
                    else:
                        data = '{"storeId":' + '"' + str(storeId) + '"' + ',"categoryIds":"[' + str(cat3Id) + ']","type":1,"pn":' + str(i) + ',"rn":20,"rankId":' +'"'+ str(rankId) +'"'+ ',"sortBy":"","isShowGuessLike":"0","isRankByAlg":"0","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"cityId":'+str(city_id)+',"bizChannel":"mobile.antispider.default"}'
                        sign_t = get_sign(data, cookie)
                        sign = sign_t[0]
                        t = sign_t[1]
                        # print(data)
                        send_request(sign, cookie, data, t)


if __name__ == '__main__':
    main_druginfo()



