---
nl: Which census block group in San Francisco has the highest median household income?
sql: WITH san_francisco AS (SELECT i.CENSUS_BLOCK_GROUP, i.B19013e1 AS median_household_income_2019_usd
  FROM census_2019_income AS i WHERE SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2) = '06'
  AND SUBSTRING(i.CENSUS_BLOCK_GROUP, 3, 3) = '075' AND i.B19013e1 IS NOT NULL), highest
  AS (SELECT MAX(median_household_income_2019_usd) AS highest_income FROM san_francisco)
  SELECT s.CENSUS_BLOCK_GROUP, s.median_household_income_2019_usd FROM san_francisco
  AS s CROSS JOIN highest AS h WHERE s.median_household_income_2019_usd = h.highest_income
  ORDER BY s.CENSUS_BLOCK_GROUP
source: user
tags:
- source:verified-census-query
---
