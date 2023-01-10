import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import cert_info

# 친환경농산물 가격정보('05~'20.3.)
# 요청URL: https://www.kamis.or.kr/service/price/xml.do?action=periodNaturePriceList
def kamis_api_5(startday = '2015-10-07', endday = '2015-11-26', itemcategorycode = '200', itemcode = '212', kindcode = '00' , productrankcode = '07', countycode = '1101', convert_kg_yn = 'Y', key = '111', id = '222'):
    url = 'https://www.kamis.or.kr/service/price/xml.do?action=periodNaturePriceList'
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
        'seqnum':[],
        'countyname':[],
        'countyname1':[],
        'marketname':[],
        'unit':[],
        'regday':[],
        'price':[],
        'group_first_yn':[],
        'group_last_yn':[],
        'countyname_rowspan':[],
        'countyname_first_yn':[],
        'marketname_rowspan':[],
        'marketname_first_yn':[]
    }

### 230110 - 여기까지 작업 완료

    for i in root.findall("condition"):
        cnt = 0
        for j in i.findall("item"):
            cnt = cnt + 1
            for t in j:
                row_dict[t.tag].append(t.text)
        for j in range(1,cnt+1):
            row_dict['productclscode'].append(i.find("productclscode").text)
            row_dict['caption'].append(i.find("caption").text)

    df = pd.DataFrame(row_dict)
    df.columns =  ['부류코드','품목명','구분(연도)','평균','최대','최소','표준편차','변동계수','진폭계수']
    # print(df)

    return df