# API 6. 최근일자 도.소매가격정보(상품 기준)

import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import cert_info

# 최근일자 도.소매가격정보(상품 기준)
# 요청URL: http://www.kamis.co.kr/service/price/xml.do?action=dailySalesList&p_cert_key=test&p_cert_id=test&p_returntype=xml
def kamis_api_6(regday = '20230113'):
    url = 'http://www.kamis.co.kr/service/price/xml.do?action=dailySalesList&p_cert_key=test&p_cert_id=test&p_returntype=xml'
    params = {
        ('p_cert_key', cert_info.cert_key()), #인증Key
        ('p_cert_id', cert_info.cert_id()),   #요청자id
        ('p_returntype', 'xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
        ('p_regday', regday) #조회일자
        }
    response = requests.get(url, params)

    root = ET.fromstring(response.text)

    row_dict = {
        'product_cls_code':[],
        'product_cls_name':[],
        'category_code':[],
        'category_name':[],
        'productno':[],
        'lastest_day':[],
        'productName':[],
        'item_name':[],
        'unit':[],
        'day1':[],
        'dpr1':[],
        'day2':[],
        'dpr2':[],
        'day3':[],
        'dpr3':[],
        'day4':[],
        'dpr4':[],
        'direction':[],
        'value':[],
    }

    dt = root.find('price')

    for i in dt.findall('item'):
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    df.columns = ['구분(01:소매 02:도매)','구분이름','부류코드','부류명','품목코드','최근조사일','품목명','품목명','단위','최근조사일자','최근조사일자(가격)','1일전일자','1일전가격','1개월전일자','1개월전가격','1년전일자','1년전가격','등락여부(0:가격하락 1:가격상승 2:등락없음)','등락율']
    # print(df)

    return df

kamis_api_6()