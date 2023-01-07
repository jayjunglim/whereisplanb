# 목표
- 2022(update)
    1. 은지님
        1. 분석프로젝트의 예시는 결과가 나오는 것을 원한다. 시작과 끝이 있는 것
        2. 분석+엔지니어링 부분을 강화하고싶다. 언어나 분야 더 깊은 sql
        ex. dbt, airflow, python
        3. (2022) 웹사이트 결과물로 실제로프로덕트나 서비스가 있으면 좋겠다.
    2. 주연
        1. 개발에 대한 관심이 있다. but 익숙해지는데 시간이 걸릴 것 같음.
        ex. dbt or python
        2. 통계를 알고 가는것도 좋을 것 같다. 의학연구 방법론, 로지스틱, 결과 테이블
        3. (2022) 우선순위는 파이썬→ sql → 엔지니어링 개발
    3. 임정
        1. (2022) 향후 컨설팅 분석업을 위한 포트폴리오제작
            ex) API, 크롤링, 자동화, 대시보드
        2. 데이터엔지니어 역량 강화
    4. 윤영
        1. 개발역량을 더 올리고싶다. 백엔드하고있지만, 프론트엔드 중심 관심
        2. 기획부터 마케팅까지의 이어지는 구조를 작은 프로젝트에서 경험해보고싶음
- 스터디 주기
    - 격주 오프라인(2주 task)설정
    - 격주 온라인(스크럼)

# whereisplanb

농산물 유통정보 API를 통하여 장바구니 물가를 확인하는 대시보드 입니다. 
(https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=3)


아이디어 개요: https://blog.naver.com/bellepoque7/222944303592

# 구조설계
*현재 2번만 구현 됨

1. airflow에 2번 정제 프로그램 탑재 및 주기적 실행(미구현)
2. kamis에서 데이터 정제(web_api_kamis) 
3. google drive에 데이터 업로드(미구현)[(참고 link)](https://ysyblog.tistory.com/296)
4. goole drive에 있는 데이터 Google data Studio에 연결(미구현)
5. 리포트 배포(ex. e-mail, slack, 웹 등) (미구현)


## 파일 설명
- cert_info: API 인증키와 아이디 정보, 개인정보 보호를 위해 공란처리
- test.py: 파일을 실행하는 스크립트
- web_api_kamis.py: open ai를 불러오는 함수 스크립트(1번만 작동)
- web_api_garak.ipynb: 가락시장 api 현재는 사용하지 않음

### we_api_kamis.py 함수의 구조

- kamis api는 총 14개로 이루어져있음. 현재 각 API에 대한 함수를 따로 만들어 순차적으로 1번~14번으로 명칭
- 현재는 1번 API 만 정제해 놓은 상태고 이후 공통된 정제 함수를 도입해야할 듯

kamis_api_1는 1번 `일별 부류별 도.소매가격정보`의 API를 호출하는 기능으로 필요한 정보(ex. key, id, return type 등)을 입력하면 정보를 리턴해줌.
이때 데이터는 xml으로 전달되기 떄문에 다음과 같은 정제 작업이 필요함(추가 될 수 있음)
1. iteration을 이용하여 Dataframe 으로 정제
2. 모든 date type을 object -> string 변환
3. 가격 value '-'  ->  NaN으로 변환
4. 가격 value ',' 제거
5. 가격 data type -> Numeric으로 변환

최종 조회한 품목 코드만 dataframe 형태로 return

### 해결해야할 문제
1. 가격조회 시 특정한 날짜(ex 5월1일)에 가격이 나오지 않는 경우
- A) 전후 1일 가격으로 대치(2월1일, 1월 31일 둘다 가격 공란)
- B) 전후 일주일 가격 평균으로 대치
