-- sheet1

SELECT *
FROM public.kamis_sheet1 ks 

select *
from public.kamis_lt1


-- DDL

CREATE TABLE public.kamis_lt1(
	item_category_cd INT NOT NULL,		-- 부류코드
    item_category_nm VARCHAR NOT null	-- 부류명
);


-- 추출 쿼리 SQL

WITH kamis_lt1 as (
	SELECT  
		"부류코드"::int AS item_category_cd,
		"부류명"::varchar AS item_category_nm
	FROM
		public.kamis_sheet1
)
INSERT INTO public.kamis_lt1 (
   item_category_cd, item_category_nm
)
SELECT
    item_category_cd, item_category_nm
FROM
    kamis_lt1;
