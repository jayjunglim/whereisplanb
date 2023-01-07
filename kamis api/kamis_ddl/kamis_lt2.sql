-- sheet2

SELECT *
FROM public.kamis_sheet2 ks

select *
from public.kamis_lt2


-- DDL

CREATE TABLE public.kamis_lt2(
	item_category_cd INT NOT NULL,	-- 부류코드
    item_cd int NOT null,			-- 품목코드
	item_nm varchar not null		-- 품목명
);


-- 추출 쿼리 SQL

WITH kamis_lt2 as (
	SELECT  
		"부류코드"::int AS item_category_cd,
		"품목코드"::int as item_cd,
		"품목명"::varchar AS item_nm
	FROM
		public.kamis_sheet2
)
INSERT INTO public.kamis_lt2 (
   item_category_cd, item_cd, item_nm
)
SELECT
    item_category_cd, item_cd, item_nm
FROM
    kamis_lt2;
    