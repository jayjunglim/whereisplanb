-- sheet4

SELECT *
FROM public.kamis_sheet4 ks 

select *
from public.kamis_lt4


-- DDL

CREATE TABLE public.kamis_lt4(
	item_group_cd INT NOT NULL,			-- 품목그룹코드
    item_group_nm varchar NOT null,		-- 품목그룹명
	item_cd int not null,				-- 품목코드
	item_nm varchar not null,			-- 품목명
	kind_cd int null,					-- 품종코드
	kind_nm varchar null,				-- 품종명
	wholesale_un varchar null,			-- 도매출하단위
	wholesale_un_size int null,			-- 도매출하단위크기	
	retail_un varchar null,				-- 소매출하단위
	retail_un_size int null,			-- 소매출하단위크기
	organic_un_old varchar null,		-- 친환경농산물출하단위('05~'20.3)
	organic_un_size_old int null,		-- 친환경농산물출하단위크기('05~'20.3)
	organic_un_new varchar null,		-- 친환경농산물출하단위('20.4~)
	organic_un_size_new int null,		-- 친환경농산물출하단위크기('20.4~)
	wholesale_graderank varchar null,	-- 도매등급
	retail_graderank varchar null,		-- 소매등급
	organic_graderank_old varchar null,	-- 친환경등급('05~'20.3)
	organic_graderank_new varchar null	-- 친환경등급('20.4~)
);


-- 추출 쿼리 SQL

WITH kamis_lt4 as (
	SELECT  
	    "품목 그룹코드"::int as item_group_cd,
	    "품목 그룹명"::varchar as item_group_nm,
	    "품목 코드"::int as item_cd,
	    "품목명"::varchar as item_nm,
	   	"품종코드"::int as kind_cd,
	    "품종명"::varchar as kind_nm,
	    "도매출하단위"::varchar as wholesale_un,
	    "도매출하단위 크기"::int as wholesale_un_size,
	    "소매출하단위"::varchar as	retail_un,
	    "소매출하단위 크기"::int as retail_un_size,
	    "친환경농산물출하단위('05~'20.3)"::varchar as organic_un_old,
	    "친환경농산물출하단위크기('05~'20.3)"::int as organic_un_size_old,
	    "친환경농산물출하단위('20.4~)"::varchar as organic_un_new,
	    "친환경농산물출하단위크기('20.4~)"::int as organic_un_size_new,
	    "도매 등급"::varchar as wholesale_graderank,
	    "소매 등급"::varchar as retail_graderank,
	    "친환경 등급('05~'20.3)"::varchar as organic_graderank_old,
	    "친환경 등급('20.4~)"::varchar as organic_graderank_new
	FROM
		public.kamis_sheet4
)
INSERT INTO kamis_lt4 (
	item_group_cd, item_group_nm, item_cd, item_nm, kind_cd, kind_nm,
	wholesale_un, wholesale_un_size, retail_un, retail_un_size,
	organic_un_old, organic_un_size_old, organic_un_new, organic_un_size_new,
	wholesale_graderank, retail_graderank, organic_graderank_old, organic_graderank_new
)
SELECT
	item_group_cd, item_group_nm, item_cd, item_nm, kind_cd, kind_nm,
	wholesale_un, wholesale_un_size, retail_un, retail_un_size,
	organic_un_old, organic_un_size_old, organic_un_new, organic_un_size_new,
	wholesale_graderank, retail_graderank, organic_graderank_old, organic_graderank_new
FROM
    kamis_lt4;
    