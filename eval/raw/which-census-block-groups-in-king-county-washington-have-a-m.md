---
nl: Which census block groups in King County, Washington have a median household income
  above $150,000?
sql: SELECT i.CENSUS_BLOCK_GROUP, i.B19013e1 AS median_household_income_2019_usd FROM
  census_2019_income AS i JOIN census_2019_county_fips AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'WA' AND f.COUNTY = 'King County' AND i.B19013e1 > 150000 ORDER BY median_household_income_2019_usd
  DESC, i.CENSUS_BLOCK_GROUP
source: user
tags:
- source:verified-census-query
---
