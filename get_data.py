import pandas
from openpyxl import Workbook
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()
wb = Workbook(write_only=True)
sheet = wb.create_sheet('eleme')

def get_shop_info():
    sql = 'select * from e_shop_info'
    cursor.execute(sql)
    all_info = cursor.fetchall()
    row = ['storeId', 'shopName', 'monthSales', 'shopScore', 'address', 'activity', 'coupon', 'category', 'categoryIds',
           'city']
    sheet.append(row=row)
    for info in all_info:
        storeId = info[0]
        shopName = info[1]
        monthSales = info[2]
        shopScore = info[3]
        address = info[4]
        activity = info[5]
        coupon = info[6]
        category = info[7]
        categoryIds = info[8]
        city = info[9]
        row = [storeId, shopName, monthSales, shopScore, address, activity, coupon, category, categoryIds, city]
        sheet.append(row=row)

def get_shop():
    sql = 'select * from ele_shop'
    cursor.execute(sql)
    all_info = cursor.fetchall()
    row = ['storeId', 'shopName', 'monthSales', 'shopScore', 'eleId', 'wid']
    sheet.append(row=row)
    for info in all_info:
        storeId = info[0]
        shopName = info[1]
        monthSales = info[2]
        shopScore = info[3]
        eleId = info[4]
        wid = info[5]
        row = [storeId, shopName, monthSales, shopScore, eleId, wid]
        sheet.append(row)

    file = 'D:\\top50\\ele_shop.xlsx'
    wb.save(file)

get_shop()