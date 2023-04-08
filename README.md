# whereisplanb

- [농산물 유통정보 API](https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=3)를 통하여 장바구니 물가를 확인하는 대시보드 프로젝트입니다.
- [아이디어 개요](https://blog.naver.com/bellepoque7/222944303592)


## 구조설계

1. airflow에 2번 정제 프로그램 탑재 및 주기적 실행
2. kamis data api 크롤링 및 데이터 적재
3. 대시보드화 

## 디렉토리
- cert_info: API 인증키와 아이디 정보, 개인정보 보호를 위해 공란처리
- web_api_kamis.py: open ai를 불러오는 함수
 - Data
  - category_detail_code.csv: 상품별 코드맵핑
  - 상품명_날짜: 해당 날짜 기준 데이터 크롤링

### we_api_kamis.py 함수의 구조

- kamis api는 총 14개로 이루어져있음. 현재 각 API에 대한 함수를 따로 만들어 순차적으로 1번~14번으로 명칭

kamis_api_1는 1번 `일별 부류별 도.소매가격정보`의 API를 호출하는 기능으로 필요한 정보(ex. key, id, return type 등)을 입력하면 DataFrame으로 
- 정제 작업 절차
1. iteration을 이용하여 Dataframe 으로 정제
2. 모든 date type을 object -> string 변환
3. 가격 value '-'  ->  NaN으로 변환
4. 가격 value ',' 제거
5. 가격 data type -> Numeric으로 변환
