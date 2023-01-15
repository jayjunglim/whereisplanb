# API 12. 친환경농산물 가격정보('20.4.)

import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import cert_info

# 친환경농산물 가격정보('20.4.)
# 요청URL: http://www.kamis.or.kr/service/price/xml.do?action=periodEcoPriceList
def kamis_api_12(startday = '2020-05-01', endday = '2020-07-01', itemcategorycode = '200', itemcode = '212', kindcode = '00' , productrankcode = '07', countycode = '1101', convert_kg_yn = 'Y', key = '111', id = '222'):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodEcoPriceList'
    params = {
        ('p_cert_key', cert_info.cert_key()), #인증Key
        ('p_cert_id', cert_info.cert_id()),   #요청자id
        ('p_returntype', 'xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
        ('p_startday', startday), #조회기간(start date)
        ('p_endday', endday), #조회기간(end date)
        ('p_itemcategorycode', itemcategorycode), #부류코드
        ('p_itemcode', itemcode), #품목코드
        ('p_kindcode', kindcode), #품종코드
        ('p_productrankcode', productrankcode), #등급코드
        ('p_countrycode', countycode), #시군구코드
        ('p_covert_kg_yn', convert_kg_yn), #kg단위 환산여부
        ('p_key', key),
		('p_id', id)
        }
    response = requests.get(url, params)

    root = ET.fromstring(response.text)

    row_dict = {
        'countyname':[],
        'marketname':[],
        'unit':[],
        'regday':[],
        'price':[]
    }

    dt = root.find('data')

    for i in dt.findall('item'):
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    df.columns = ['시군구','마켓명','단위','일자','가격']
    # print(df)

    return df

kamis_api_12()