---
nl: How many households in San Francisco County, California have an annual income
  above ,000?
sql: SELECT SUM(i.B19001e14) + SUM(i.B19001e15) + SUM(i.B19001e16) + SUM(i.B19001e17)
  AS estimated_households_income_100k_or_more FROM census_2019_income AS i JOIN census_2019_county_fips
  AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'CA' AND f.COUNTY = 'San Francisco County'
source: user
tags:
- source:verified-census-query
---
