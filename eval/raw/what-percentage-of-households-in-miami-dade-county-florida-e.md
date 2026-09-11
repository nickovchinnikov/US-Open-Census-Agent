---
nl: What percentage of households in Miami-Dade County, Florida earn more than $100,000
  per year?
sql: SELECT 100.0 * (SUM(i.B19001e14) + SUM(i.B19001e15) + SUM(i.B19001e16) + SUM(i.B19001e17))
  / NULLIF(SUM(i.B19001e1), 0) AS households_income_100k_or_more_pct FROM census_2019_income
  AS i JOIN census_2019_county_fips AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'FL' AND f.COUNTY = 'Miami-Dade County'
source: user
tags:
- source:verified-census-query
---
