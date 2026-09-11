---
nl: Which census block group in New York County, New York has the highest median household
  income?
sql: WITH new_york_county AS (SELECT i.CENSUS_BLOCK_GROUP, i.B19013e1 AS median_household_income_2019_usd
  FROM census_2019_income AS i JOIN census_2019_county_fips AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'NY' AND f.COUNTY = 'New York County' AND i.B19013e1 IS NOT NULL), highest
  AS (SELECT MAX(median_household_income_2019_usd) AS highest_income FROM new_york_county)
  SELECT n.CENSUS_BLOCK_GROUP, n.median_household_income_2019_usd FROM new_york_county
  AS n CROSS JOIN highest AS h WHERE n.median_household_income_2019_usd = h.highest_income
  ORDER BY n.CENSUS_BLOCK_GROUP
source: user
tags:
- source:verified-census-query
---
