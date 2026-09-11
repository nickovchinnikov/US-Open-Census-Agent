---
nl: Which census block group in Los Angeles County, California has the lowest median
  household income?
sql: WITH los_angeles_county AS (SELECT i.CENSUS_BLOCK_GROUP, i.B19013e1 AS median_household_income_2019_usd
  FROM census_2019_income AS i JOIN census_2019_county_fips AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'CA' AND f.COUNTY = 'Los Angeles County' AND i.B19013e1 IS NOT NULL),
  lowest AS (SELECT MIN(median_household_income_2019_usd) AS lowest_income FROM los_angeles_county)
  SELECT l.CENSUS_BLOCK_GROUP, l.median_household_income_2019_usd FROM los_angeles_county
  AS l CROSS JOIN lowest AS x WHERE l.median_household_income_2019_usd = x.lowest_income
  ORDER BY l.CENSUS_BLOCK_GROUP
source: user
tags:
- source:verified-census-query
---
