import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import cert_info

#https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=1
def kamis_api_1(cls_code ='02', category_detail_code ='224', country_code ='',regday='2022-12-01',convert_kg_yn ='N'):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList'
    params = {
    ('p_cert_key',cert_info.cert_key()), #인증Key
    ('p_cert_id',cert_info.cert_id()),   #요청자id
    ('p_returntype','xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
    ('p_product_cls_code',cls_code), #구분 ( 01:소매, 02:도매, default:02 )
    ('p_item_category_code', category_detail_code[0]+'00'), # 부류코드(100:식량작물, 200:채소류, 300:특용작물, 400:과일류, 500:축산물, 600:수산물, default:100)
    ('p_country_code',country_code), 
    #* 소매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2300:인천, 2401:광주, 2501:대전, 2601:울산, 3111:수원, 3211:춘천, 3311:청주, 3511:전주, 
    # 3711:포항, 3911:제주, 3113:의정부, 3613:순천, 3714:안동, 3814:창원, 3145:용인)
    #도매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2401:광주, 2501:대전)default : 전체지역
    ('p_regday',regday), # 날짜 : yyyy-mm-dd (default : 최근 조사일자)
    ('p_convert_kg_yn',convert_kg_yn), #kg단위 환산여부(Y : 1kg 단위표시, N : 정보조사 단위표시, ex: 쌀 20kg)default : N
    }
    response = requests.get(url,params)
    root = ET.fromstring(response.text)
    row_dict = {'item_name':[],'item_code':[],'kind_name':[],'kind_code':[],'rank':[],'rank_code':[],
    'unit':[],'day1':[],'dpr1':[],'day2':[],'dpr2':[],'day3':[],'dpr3':[],'day4':[],'dpr4':[],'day5':[],'dpr5':[]
    ,'day6':[],'dpr6':[],'day7':[],'dpr7':[]}
    #data/item 계층 밑의 값을 list으로 가져와 iteration
    for i in root.findall('./data/item'):
        # item_name부터 텍스트를 가져와 딕셔너리에 저장
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    
    df.columns =  ['품목명','품목코드','품종명','품종코드','상태(상품, 중품)','상태코드',
    '단위','일자(조회일자)','조회일자 가격','1일전 일자(조회일자 기준)','1일전 가격','1주일전 일자(조회일자 기준)'
    ,'1주일전 가격','2주일전 일자(조회일자 기준)','2주일전 가격','1개월전 일자(조회일자 기준)','1개월전 가격','1년전 일자(조회일자 기준)','1년전 가격','평년일자','평년 가격']
    
    #조회일자 기준 데이터가 없으면 함수 종료
    if df.empty:
        return df
    else:
        #Seires의 데이터타입 object -> string
        df = df.convert_dtypes()
        # 가격부분의 '-'를 NaN으로 변경
        df['조회일자 가격'] = df['조회일자 가격'].replace('-',np.NaN)
        df['1일전 가격'] = df['1일전 가격'].replace('-',np.NaN)
        df['1주일전 가격'] = df['1주일전 가격'].replace('-',np.NaN)
        df['2주일전 가격'] = df['2주일전 가격'].replace('-',np.NaN)
        df['1개월전 가격'] = df['1개월전 가격'].replace('-',np.NaN)
        df['1년전 가격'] = df['1년전 가격'].replace('-',np.NaN)
        df['평년 가격'] = df['평년 가격'].replace('-',np.NaN)
    
        # 가격의 , 부분을 바꾸고 numeric으로 변경
        df['조회일자 가격'] = df['조회일자 가격'].str.replace(',','').apply(pd.to_numeric)
        df['1일전 가격'] = df['1일전 가격'].str.replace(',','').apply(pd.to_numeric)
        df['1주일전 가격'] = df['1주일전 가격'].str.replace(',','').apply(pd.to_numeric)
        df['2주일전 가격'] = df['2주일전 가격'].str.replace(',','').apply(pd.to_numeric)
        df['1개월전 가격'] = df['1개월전 가격'].str.replace(',','').apply(pd.to_numeric)
        df['1년전 가격'] = df['1년전 가격'].str.replace(',','').apply(pd.to_numeric)
        df['평년 가격'] = df['평년 가격'].str.replace(',','').apply(pd.to_numeric)
        
        return df[df['품목코드']==category_detail_code] 


#https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=2
#데이터 함수 만드는 것
#2번 코드가 일반 적임.
def kamis_api_2(startday='2022-01-01',endday ='2022-12-01',productclscode = '02',itemcategorycode ='',
itemcode ='',kindcode = '', productrankcode='',countrycode=''):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList'
    params = {
    ('p_cert_key',cert_info.cert_key()), #인증Key
    ('p_cert_id',cert_info.cert_id()),   #요청자id
    ('p_returntype','xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
    ('p_startday',startday), #조회기간(start date)
    ('p_endday',endday), #조회기간(end date)
    ('p_productclscode',productclscode), #구분 ( 01:소매, 02:도매, default:02 )
    ('p_itemcategorycode',itemcategorycode), #부류코드
    ('p_itemcode',itemcode), #품목코드
    ('p_kindcode',kindcode), #품종코드
    ('p_productrankcode',productrankcode), #등급코드
    ('p_countrycode',countrycode),
    #소매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2300:인천, 2401:광주, 2501:대전, 2601:울산, 3111:수원, 3211:춘천, 3311:청주, 3511:전주, 3711:포항, 3911:제주, 3113:의정부, 3613:순천, 3714:안동, 3814:창원, 3145:용인) 
    #도매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2401:광주, 2501:대전)
    #default : 전체지역
    ('p_convert_kg_yn','')
    }
    response = requests.get(url,params)
    print(response.text)
    #여기까지만 출력해도 충분
    root = ET.fromstring(response.text)
    row_dict = {'itemname':[],'kindname':[],'countyname':[],'marketname':[],'yyyy':[],'regday':[],
    'price':[]}
    #data/item 계층 밑의 값을 list으로 가져와 iteration
    for i in root.findall('./data/item'):
        # item_name부터 텍스트를 가져와 딕셔너리에 저장
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    df.columns =  ['품목명','품종명','시군구','마켓명','연도','날짜','가격']

    return df

#https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=3
def kamis_api_3(yyyy = '2022',period ='3',itemcode ='111',kindcode ='01',graderank ='2',countycode='1101',convert_kg_yn ='N',itemcategorycode='100'):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=monthlySalesList'
    params = {
    ('p_cert_key',cert_info.cert_key()), #인증Key
    ('p_cert_id',cert_info.cert_id()),   #요청자id
    ('p_returntype','xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
    ('p_yyyy',yyyy), #연도 설정
    ('p_period',period), #기간 설정(default : 3년)
    ('p_itemcode',itemcode), #품목코드
    ('p_kindcode',kindcode), #품종코드s
    ('p_graderank',graderank), #등급(상품,중품)
    ('p_countycode',countycode), #시군구
    ('p_convert_kg_yn',convert_kg_yn), #Kg단위 환산여부
    ('p_itemcategorycode',itemcategorycode) #부류코드
    }
    response = requests.get(url,params)
    # print(response.text)
    root = ET.fromstring(response.text)
    row_dict = {
        'productclscode':[],'caption':[],
        'yyyy':[],'m1':[],'m2':[],'m3':[],'m4':[],'m5':[],'m6':[],'m7':[],'m8':[],'m9':[],'m10':[],'m11':[],'m12':[],'yearavg':[]}
    for i in root.findall('./price/item'):
        #productclscode, caption은 년도만큼만 반복되므로 따로 dictionary에 삽입
        row_dict['productclscode'].append(root.find('./price/productclscode').text)
        row_dict['caption'].append(root.find('./price/caption').text)
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    # caption 컬럼 > 기준으로 분리: 캡션1~캡션5
    df = pd.DataFrame(row_dict)
    df[['캡션1','캡션2','캡션3','캡션4','캡션5','캡션6']] = df['caption'].str.split(' > ', n=6,expand=True)
    df.drop('caption', axis=1, inplace=True)

    df.columns =  ['구분','연도','1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월','연평균','캡션1','캡션2','캡션3','캡션4','캡션5','캡션6']
    return df

# 연도별 도소매가격정보
# 요청URL: http://www.kamis.or.kr/service/price/xml.do?action=yearlySalesList
def kamis_api_4(yyyy = '2015', itemcategorycode = '100', itemcode = '111', kindcode = '01', graderank = '1', countycode = '1101', convert_kg_yn = 'N'):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=yearlySalesList'
    params = {
        ('p_cert_key', cert_info.cert_key()), #인증Key
        ('p_cert_id', cert_info.cert_id()),   #요청자id
        ('p_returntype', 'xml'), #Return Type (json:Json 데이터 형식, xml:XML데이터형식)
        ('p_yyyy', yyyy), #연도 설정
        ('p_itemcategorycode', itemcategorycode), #부류코드
        ('p_itemcode', itemcode), #품목코드
        ('p_kindcode', kindcode), #품종코드s
        ('p_graderank', graderank), #등급(상품,중품)
        ('p_countycode', countycode), #시군구
        ('p_convert_kg_yn', convert_kg_yn), #Kg단위 환산여부 
        }
    response = requests.get(url, params)

    root = ET.fromstring(response.text)

    row_dict = {
        'productclscode':[],
        'caption':[],
        'div':[],
        'avg_data':[],
        'max_data':[],
        'min_data':[],
        'stddev_data':[],
        'cv_data':[],
        'af_data':[]
    }

    for i in root.findall("price"):
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
 
 #이주연일함