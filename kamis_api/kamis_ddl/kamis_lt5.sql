-- sheet5

SELECT *
FROM public.kamis_sheet5 ks 

select *
from public.kamis_lt5


-- DDL

CREATE TABLE public.kamis_lt5(
	p_productrank_cd INT NOT NULL,	-- 등급코드(p_productrankcode)
    p_graderank_cd int NOT NULL,	-- 등급코드(p_graderank)
    graderank_nm varchar NOT NULL	-- 등급코드명
);


-- 추출 쿼리 SQL

WITH kamis_lt5 as (
	SELECT  
	    "등급코드(p_productrankcode)"::int as p_productrank_cd,
	    "등급코드(p_graderank)"::int as p_graderank_cd,
	    "등급코드명"::varchar as graderank_nm
	FROM
		public.kamis_sheet5
)
INSERT INTO kamis_lt5 (
	p_productrank_cd, p_graderank_cd, graderank_nm
)
SELECT
	p_productrank_cd, p_graderank_cd, graderank_nm
FROM
    kamis_lt5;
    